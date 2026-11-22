using System.Diagnostics;

namespace Parcial2.VarianteB;

public interface IReceptorPedidos
{
    void Registrar(string pedido, int plazoMinutos);   // llega un pedido (nombres únicos)
    string? PrepararSiguiente();                       // saca y devuelve el de menor plazo; null si no hay ninguno
    bool EstaPendiente(string pedido);                 // ¿este pedido sigue pendiente? (prepararlo lo saca)
    int Pendientes { get; }                            // cuántos hay pendientes
}

public sealed record Pedido(string Nombre, int Plazo, int Llegada);

// ---------- SOLUCIÓN INGENUA (lista simple): correcta pero lenta ----------
public sealed class ReceptorIngenuo : IReceptorPedidos
{
    private readonly List<Pedido> _lista = new();
    private int _llegadas;

    public void Registrar(string pedido, int plazoMinutos) => _lista.Add(new Pedido(pedido, plazoMinutos, _llegadas++));

    public string? PrepararSiguiente()
    {
        if (_lista.Count == 0) return null;
        int mejor = 0;
        for (int i = 1; i < _lista.Count; i++)
        {
            var p = _lista[i]; var m = _lista[mejor];
            if (p.Plazo < m.Plazo || (p.Plazo == m.Plazo && p.Llegada < m.Llegada)) mejor = i;
        }
        string nombre = _lista[mejor].Nombre;
        _lista.RemoveAt(mejor);
        return nombre;
    }

    public bool EstaPendiente(string pedido)
    {
        foreach (var p in _lista) if (p.Nombre == pedido) return true;
        return false;
    }

    public int Pendientes => _lista.Count;
}

// ---------- TU SOLUCIÓN: elige la(s) estructura(s) y escríbela aquí ----------
// --- Se usara usar hash y Una PriorityQueue (o cola de prioridad) es una estructura de datos en la que cada elemento tiene una prioridad asociada 
// --- y se extrae primero según esa prioridad, en lugar de seguir el orden de llegada (FIFO) de una cola normal
public sealed class ReceptorMejorado : IReceptorPedidos
{
    private readonly PriorityQueue<Pedido, (int plazo, int llegada)> _cola = new();
    private readonly HashSet<string> _pendientes = new();
    private int _llegadas;
    public void Registrar(string pedido, int plazoMinutos)
    {
        var nuevo = new Pedido(pedido, plazoMinutos, _llegadas++);

        _cola.Enqueue(
            nuevo,
            (nuevo.Plazo, nuevo.Llegada)
        );

        _pendientes.Add(pedido);
    }

    public string? PrepararSiguiente()
    {if (_cola.Count == 0)
            return null;
        Pedido pedido = _cola.Dequeue();
        _pendientes.Remove(pedido.Nombre);
        return pedido.Nombre;}
    public bool EstaPendiente(string pedido)
    {return _pendientes.Contains(pedido);}
    public int Pendientes
    {get { return _cola.Count; }}}
public static class Programa
{
    // El guion de pruebas: cada paso es (operación, argumento, plazo, resultado esperado).
    private static readonly (string op, string arg, int plazo, string esperado)[] Guion =
    {
        ("registrar", "Torta", 120, ""), ("registrar", "Galletas", 30, ""), ("registrar", "Pan", 120, ""), ("registrar", "Brazo", 60, ""),
        ("pendientes", "", 0, "4"),
        ("esta", "Galletas", 0, "True"), ("esta", "Flan", 0, "False"),
        ("preparar", "", 0, "Galletas"), ("esta", "Galletas", 0, "False"),
        ("preparar", "", 0, "Brazo"),
        ("registrar", "Alfajor", 30, ""),
        ("preparar", "", 0, "Alfajor"), ("preparar", "", 0, "Torta"), ("preparar", "", 0, "Pan"),
        ("preparar", "", 0, "(ninguno)"), ("pendientes", "", 0, "0"),
    };

    private static string Ejecutar(IReceptorPedidos g, string op, string arg, int plazo)
    {
        switch (op)
        {
            case "registrar": g.Registrar(arg, plazo); return "";
            case "preparar": return g.PrepararSiguiente() ?? "(ninguno)";
            case "esta": return g.EstaPendiente(arg).ToString();
            default: return g.Pendientes.ToString();
        }
    }

    private static void Probar(string titulo, IReceptorPedidos g)
    {
        int bien = 0, total = 0;
        try
        {
            foreach (var (op, arg, plazo, esperado) in Guion)
            {
                string obtenido = Ejecutar(g, op, arg, plazo);
                if (op == "registrar") continue;
                total++;
                if (obtenido == esperado) bien++;
                else Console.WriteLine($"   MAL en «{op} {arg}»: esperado {esperado}, obtuvo {obtenido}");
            }
            Console.WriteLine($"{titulo}: {bien} de {total} pasos correctos");
        }
        catch (NotImplementedException) { Console.WriteLine($"{titulo}: (sin escribir todavía)"); }
    }

    // La CARGA para medir: n pedidos llegan y después se preparan los n.
    public static long EjecutarCarga(IReceptorPedidos g, int n)
    {
        for (int i = 0; i < n; i++) g.Registrar("Q" + i, ((int)((i * 6007L) % 6) + 1) * 15);
        long control = 0;
        for (int i = 0; i < n; i++) control += g.PrepararSiguiente()!.Length;
        return control;
    }

    public static void Main()
    {
        Probar("ReceptorIngenuo ", new ReceptorIngenuo());
        Probar("ReceptorMejorado", new ReceptorMejorado());

        // Una medición de ejemplo, SIN protocolo (el protocolo lo agregas tú en tu medición):
        var reloj = Stopwatch.StartNew();
        EjecutarCarga(new ReceptorIngenuo(), 10_000);
        Console.WriteLine($"Ingenuo con 10.000 pedidos: {reloj.ElapsedMilliseconds} ms (una sola medición: no es evidencia)");
    }
}
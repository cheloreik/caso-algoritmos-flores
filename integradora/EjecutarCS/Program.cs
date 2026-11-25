using System.Diagnostics;

namespace Integradora.VarianteA;

public sealed record Paquete(string Codigo, int Kg, int Ganancia);

public interface IPlanificador
{
    (int ganancia, List<string> codigos) Elegir(Paquete[] paquetes, int capacidadKg);
    bool EstaEnElViaje(string codigo);
}

// ---------- SOLUCIÓN INGENUA ----------
public sealed class PlanificadorIngenuo : IPlanificador
{
    private List<string> _elegidos = new();

    public (int ganancia, List<string> codigos) Elegir(Paquete[] paquetes, int capacidadKg)
    {
        int n = paquetes.Length, mejor = 0;
        long mejorMascara = 0;

        for (long mascara = 0; mascara < (1L << n); mascara++)
        {
            int kg = 0, ganancia = 0;

            for (int i = 0; i < n; i++)
            {
                if ((mascara & (1L << i)) != 0)
                {
                    kg += paquetes[i].Kg;
                    ganancia += paquetes[i].Ganancia;
                }
            }

            if (kg <= capacidadKg && ganancia > mejor)
            {
                mejor = ganancia;
                mejorMascara = mascara;
            }
        }

        _elegidos = new List<string>();

        for (int i = 0; i < n; i++)
        {
            if ((mejorMascara & (1L << i)) != 0)
                _elegidos.Add(paquetes[i].Codigo);
        }

        return (mejor, new List<string>(_elegidos));
    }

    public bool EstaEnElViaje(string codigo)
    {
        return _elegidos.Contains(codigo);
    }
}

// ---------- SOLUCIÓN MEJORADA ----------
public sealed class PlanificadorMejorado : IPlanificador
{
    private HashSet<string> _elegidos = new();

    public (int ganancia, List<string> codigos) Elegir(
        Paquete[] paquetes,
        int capacidadKg)
    {
        int n = paquetes.Length;

        int[,] dp = new int[n + 1, capacidadKg + 1];

        for (int i = 1; i <= n; i++)
        {
            var paquete = paquetes[i - 1];

            for (int w = 0; w <= capacidadKg; w++)
            {
                dp[i, w] = dp[i - 1, w];

                if (paquete.Kg <= w)
                {
                    dp[i, w] = Math.Max(
                        dp[i, w],
                        dp[i - 1, w - paquete.Kg] + paquete.Ganancia
                    );
                }
            }
        }

        _elegidos.Clear();

        int capacidadActual = capacidadKg;

        for (int i = n; i > 0; i--)
        {
            if (dp[i, capacidadActual] != dp[i - 1, capacidadActual])
            {
                var paquete = paquetes[i - 1];

                _elegidos.Add(paquete.Codigo);
                capacidadActual -= paquete.Kg;
            }
        }

        return (
            dp[n, capacidadKg],
            _elegidos.ToList()
        );
    }

    public bool EstaEnElViaje(string codigo)
    {
        return _elegidos.Contains(codigo);
    }
}

public static class Programa
{
    private static Paquete[] Lote(params (string c, int kg, int g)[] datos)
        => datos.Select(d => new Paquete(d.c, d.kg, d.g)).ToArray();

    private static readonly (
        string que,
        Paquete[] paquetes,
        int capacidad,
        int esperada,
        string[] codigos
    )[] Casos =
    {
        ("el voraz se equivoca",
            Lote(("P1",10,60),("P2",20,100),("P3",30,120)),
            50,
            220,
            new[] {"P2","P3"}),

        ("cuatro paquetes",
            Lote(("P1",2,3),("P2",3,4),("P3",4,5),("P4",5,6)),
            8,
            10,
            new[] {"P2","P4"}),

        ("capacidad cero",
            Lote(("P1",5,10),("P2",7,12)),
            0,
            0,
            Array.Empty<string>()),

        ("sin paquetes",
            Lote(),
            30,
            0,
            Array.Empty<string>()),

        ("nada cabe",
            Lote(("P1",40,90),("P2",50,100)),
            30,
            0,
            Array.Empty<string>()),

        ("entran todos",
            Lote(("P1",5,10),("P2",7,12),("P3",3,4)),
            100,
            26,
            new[] {"P1","P2","P3"})
    };

    private static void Probar(string titulo, Func<IPlanificador> fabrica)
    {
        int bien = 0, total = 0;

        foreach (var (que, paquetes, capacidad, esperada, codigos) in Casos)
        {
            var plan = fabrica();

            var (ganancia, elegidos) =
                plan.Elegir(paquetes, capacidad);

            total++;

            bool ok =
                ganancia == esperada
                && elegidos.OrderBy(x => x)
                    .SequenceEqual(codigos.OrderBy(x => x));

            if (ok)
                bien++;
            else
                Console.WriteLine($"MAL en {que}");
        }

        var p = fabrica();

        p.Elegir(Casos[0].paquetes, Casos[0].capacidad);

        total += 2;

        if (p.EstaEnElViaje("P2"))
            bien++;

        if (!p.EstaEnElViaje("P1"))
            bien++;

        Console.WriteLine($"{titulo}: {bien} de {total} pruebas correctas");
    }

    public static int EjecutarCarga(IPlanificador plan, int n)
    {
        var azar = new Random(n);

        var paquetes = Enumerable
            .Range(0, n)
            .Select(i =>
                new Paquete(
                    "C" + i,
                    azar.Next(5, 60),
                    azar.Next(10, 100)))
            .ToArray();

        int capacidad = paquetes.Sum(p => p.Kg) / 3;

        var (ganancia, _) =
            plan.Elegir(paquetes, capacidad);

        return ganancia;
    }
// para los promedios 
private static double MedirPromedio(
    Func<IPlanificador> fabrica,
    int n)
{
    // Calentamiento
    EjecutarCarga(fabrica(), n);

    long total = 0;

    for (int i = 0; i < 3; i++)
    {
        var reloj = Stopwatch.StartNew();

        EjecutarCarga(fabrica(), n);

        reloj.Stop();

        total += reloj.ElapsedMilliseconds;
    }

    return total / 3.0;
}

private static void MedicionFormal()
{
    Console.WriteLine();
    Console.WriteLine("MEDICION FORMAL");
    Console.WriteLine("==============================================================");
    Console.WriteLine(
        $"{"n",-8} {"Ingenuo(ms)",-15} {"x Ant.",-10} {"Mejorado(ms)",-15} {"x Ant.",-10}");
    Console.WriteLine("--------------------------------------------------------------");

    int[] tamanios = { 18, 20, 22, 24 };

    double anteriorIngenuo = 0;
    double anteriorMejorado = 0;

    foreach (int n in tamanios)
    {
        // Verificación de ganancia
        int gananciaIngenua =
            EjecutarCarga(new PlanificadorIngenuo(), n);

        int gananciaMejorada =
            EjecutarCarga(new PlanificadorMejorado(), n);

        if (gananciaIngenua != gananciaMejorada)
        {
            Console.WriteLine(
                $"ERROR: ganancias distintas para n={n}");
            return;
        }

        double tIngenuo =
            MedirPromedio(() => new PlanificadorIngenuo(), n);

        double tMejorado =
            MedirPromedio(() => new PlanificadorMejorado(), n);

        string factorIngenuo =
            anteriorIngenuo == 0
                ? "-"
                : (tIngenuo / anteriorIngenuo).ToString("0.00");

        string factorMejorado =
            anteriorMejorado == 0
                ? "-"
                : (tMejorado / anteriorMejorado).ToString("0.00");

        Console.WriteLine(
            $"{n,-8} {tIngenuo,-15:F2} {factorIngenuo,-10} {tMejorado,-15:F2} {factorMejorado,-10}");

        anteriorIngenuo = tIngenuo;
        anteriorMejorado = tMejorado;
    }

    Console.WriteLine("==============================================================");
}
    private static long MedirTiempo(
        IPlanificador plan,
        int n,
        int repeticiones = 5)
    {
        long total = 0;

        for (int i = 0; i < repeticiones; i++)
        {
            var reloj = Stopwatch.StartNew();

            EjecutarCarga(plan, n);

            reloj.Stop();

            total += reloj.ElapsedMilliseconds;
        }

        return total / repeticiones;
    }

    private static void CompararRendimiento()
    {
        Console.WriteLine();
        Console.WriteLine("====================================================");
        Console.WriteLine("COMPARACION DE RENDIMIENTO");
        Console.WriteLine("====================================================");
        Console.WriteLine($"{"Paquetes",-12} {"Ingenuo(ms)",-15} {"Mejorado(ms)",-15}");
        Console.WriteLine("----------------------------------------------------");

        int[] tamas =  { 18, 20, 22, 24 };

        foreach (int n in tamas)
        {
            long ingenuo =
                MedirTiempo(new PlanificadorIngenuo(), n);

            long mejorado =
                MedirTiempo(new PlanificadorMejorado(), n);

            Console.WriteLine(
                $"{n,-12} {ingenuo,-15} {mejorado,-15}");
        }

        Console.WriteLine("====================================================");
    }

    public static void Main()
    {
        Probar(
            "PlanificadorIngenuo ",
            () => new PlanificadorIngenuo());

        Probar(
            "PlanificadorMejorado",
            () => new PlanificadorMejorado());

        Console.WriteLine();

        var reloj = Stopwatch.StartNew();

        EjecutarCarga(
            new PlanificadorIngenuo(),
            18);

        reloj.Stop();

        Console.WriteLine(
            $"Ingenuo con 18 paquetes: {reloj.ElapsedMilliseconds} ms");

        CompararRendimiento();
        MedicionFormal();
    }
}
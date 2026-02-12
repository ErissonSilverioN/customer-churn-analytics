using System;
using System.Collections.Generic;
using System.Text;

namespace EjerciciosLibro
{
    class Capitulo_2
    {

        public void Ejercicio_1()
        {
            int n_lados;
            float longitudLados;
            float Perimetro;
            Console.WriteLine("Cantidad de lados: ");
            n_lados = Convert.ToInt32(Console.ReadLine());
            Console.WriteLine("Longitud de lados:");
            longitudLados = Convert.ToSingle(Console.ReadLine());
            Perimetro = n_lados * longitudLados;
            Console.WriteLine("El Perimetro del poligono es: " + Perimetro);
            Console.ReadLine();
        }

        public void Ejercicio_3()
        {
            float Grados;
            float Radian;
            Console.WriteLine("Temperatura en Grados:  ");
            Grados = Convert.ToSingle(Console.ReadLine());

            Radian = Grados * ((float)Math.PI / 180);
            Console.WriteLine("La Temperatura en Radianes es: ");
            Console.ReadLine();
        }

        public void Ejercicio_5()
        {
            int Opc;
            float Dolar = 0, Euro = 0;
            float Taza = 0, Cambio = 0;

            Console.WriteLine("\n1.dolares a euro");
            Console.WriteLine("\n1.euros a dolares");
            Opc = Convert.ToInt32(Console.ReadLine());

            switch (Opc)
            {
                case 1:
                    Console.WriteLine("Digite cantidad de dolares:");
                    Dolar = Convert.ToSingle(Console.ReadLine());
                    Console.WriteLine("Taza de euros:");
                    Taza = Convert.ToSingle(Console.ReadLine());
                    Cambio = Dolar / Taza;
                    Console.WriteLine("El cambio en euros es de:" + Cambio + ":\t euros");
                    Console.ReadKey();

                    break;

                case 2:
                    Console.WriteLine("Digite cantidad de euros:");
                    Euro = Convert.ToSingle(Console.ReadLine());
                    Console.WriteLine("Taza del Dolar:");
                    Taza = Convert.ToSingle(Console.ReadLine());
                    Cambio = Euro / Taza;

                    Console.WriteLine("El cambio en dolar es de:" + Cambio + ":\tDolares");
                    Console.ReadKey();

                    break;

            }
        }

    }
}

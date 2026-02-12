using System;
using System.Collections.Generic;
using System.Text;

namespace EjerciciosLibro
{
    class Capitulo_4
    {

        public void Ejercicio4_1()
        {
            int n_numero;
            int Resultado = 0;

            Console.WriteLine("Ingrese el numero a multiplicar: ");
            n_numero = Convert.ToInt32(Console.ReadLine());

            for (int i = 0; i < 10; i++)
            {
                Resultado = n_numero * i;
                Console.WriteLine(" n_numero x" + i + "\t =" + Resultado);
            }

            Console.ReadLine();
        }

        public void Ejercicio4_2()
        {
            int n_numero;
            int Potencia;
            int Resultado = 0;
            Console.WriteLine("Ingrese el numero a elevar");
            n_numero = Convert.ToInt32(Console.ReadLine());

            Console.WriteLine("Ingrese el numero al que quiere elevar");
            Potencia = Convert.ToInt32(Console.ReadLine());

            Resultado = (int)Math.Pow(n_numero, Potencia);
            Console.WriteLine("Digite el numero de elevacion" + Resultado);
            Console.ReadKey();
        }

        public void Ejercicio4_5()
        {

            //int n;
            int Mayor = 0, Menor = 200;
            int Edad;


            for (int i = 0; i < 10; i++)
            {
                Edad = Convert.ToInt32(Console.Read());

                if (Mayor < Edad)
                {
                    Mayor = Edad;
                }
                if (Menor > Edad)
                {
                    Menor = Edad;
                }
            }


        }
    }
}

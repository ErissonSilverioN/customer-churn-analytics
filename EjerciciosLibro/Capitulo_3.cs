using System;
using System.Collections.Generic;
using System.Text;

namespace EjerciciosLibro
{
    class Capitulo_3
    {

        public void Ejercicio3_1()
        {
         float n_numero;
           // float Resultado;

            Console.WriteLine("Ingrese un numero: ");
            n_numero = Convert.ToSingle(Console.ReadLine());

            if (n_numero % 2 == 0)
            {
                Console.WriteLine("El numero ingresado es Par");
                Console.ReadLine();

            }

            else
            {
                Console.WriteLine("El numero ingresado es Impar");
                Console.ReadLine();
            }
        }


        public void Ejercicio3_4()
        {
            int n;
            Console.WriteLine("Ingrese un numero de (1-7)");
            n = Convert.ToInt32(Console.ReadLine());

            switch (n)
            {
                case 1:
                    Console.WriteLine("Domingo!!");
                    Console.ReadLine();

                    break;

                case 2:
                    Console.WriteLine("Lunes!!");
                    Console.ReadLine();

                    break;

                case 3:
                    Console.WriteLine("Martes!!");
                    Console.ReadLine();

                    break;

                case 4:
                    Console.WriteLine("Miercoles!!");
                    Console.ReadLine();

                    break;

                case 5:
                    Console.WriteLine("Jueves!!");
                    Console.ReadLine();

                    break;

                case 6:
                    Console.WriteLine("Viernes!!");
                    Console.ReadLine();

                    break;

                case 7:
                    Console.WriteLine("Sabado");
                    Console.ReadLine();

                    break;

                default:
                    Console.WriteLine("Opcion incorrecta");

                    break;
            }


        }
    }
}

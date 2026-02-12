using System;

namespace EjerciciosLibro
{
    class Program
    {
        static void Main(string[] args)
        {
            int n;
            int Opc;

            Capitulo_1 n1 = new Capitulo_1();
            Capitulo_2 n2 = new Capitulo_2();
            Capitulo_3 n3 = new Capitulo_3();
            Capitulo_4 n4 = new Capitulo_4();

            n1.Menu();
            Opc = Convert.ToInt32(Console.ReadLine());
            do
            {
                switch (Opc)
                {
                    case 1:
                        n1.Ejercicio_1();
                        Console.ReadLine();

                        break;

                    case 2:
                        n1.Menu();
                        n1.Ejercicio_5();
                        Console.ReadLine();
                        break;

                    case 3:
                        n2.Ejercicio_1();
                        Console.ReadLine();
                        break;

                    case 4:
                        n2.Ejercicio_3();
                        Console.ReadLine();
                        break;

                    case 5:
                        n2.Ejercicio_5();
                        Console.ReadLine();
                        break;

                    case 6:
                        n3.Ejercicio3_1();
                        Console.ReadLine();
                        break;

                    case 7:
                        n3.Ejercicio3_4();
                        Console.ReadLine();
                        break;

                    case 8:
                        n4.Ejercicio4_1();
                        Console.ReadLine();
                        break;

                    case 9:
                        n4.Ejercicio4_2();
                        Console.ReadLine();
                        break;

                    case 10:
                        n4.Ejercicio4_5();
                        Console.ReadLine();
                        break;

                    default:
                        Console.WriteLine("Opcion Incorrecta");
                        break;

                }

                Console.WriteLine("1-> Salir");
                n = Convert.ToInt32(Console.ReadLine());

            } while (n != 1);

        }
    }
}

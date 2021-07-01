using OfficeOpenXml;
using System;
using System.IO;
using System.Linq;

namespace DatasheetParsing
{
    class Program
    {
        static int Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.WriteLine("Please supply an excel doc filename.");
                return 1;
            }

            string excelFilename = args[0];

            using (FileStream fs = File.OpenRead(excelFilename))
            {
                ExcelPackage package = new ExcelPackage(fs);
                ExcelWorksheet general = package.Workbook.Worksheets["General"];

                Console.WriteLine(general.Name);

            }

            return 0;
        }
    }
}

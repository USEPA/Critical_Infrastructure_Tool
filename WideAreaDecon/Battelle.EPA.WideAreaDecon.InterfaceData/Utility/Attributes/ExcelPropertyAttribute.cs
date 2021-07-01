using System;
using System.Reflection;
using NPOI.SS.UserModel;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Attributes
{
    /// <summary>
    /// Attributes controlling excel parsing of a property
    /// </summary>
    [AttributeUsage(AttributeTargets.Property)]
    public class ExcelPropertyAttribute : Attribute
    {
        /// <summary>
        /// The column location of the property in the workbook
        /// </summary>
        public int Location { get; set; }

        public static ICell GetCell(Type type, string propertyName, IRow row)
        {
            var loc = type.GetProperty(propertyName)?.GetCustomAttribute<ExcelPropertyAttribute>()?.Location;
            return loc == null ? null : row.GetCell(loc.Value);
        }

        public static string GetCellValue(Type type, string propertyName, IRow row)
        {
            return GetCell(type, propertyName, row)?.ToString();
        }

        /// <summary>
        /// Constructor requiring specification of location
        /// </summary>
        /// <param name="location">The location of the parameter</param>
        public ExcelPropertyAttribute(int location)
        {
            Location = location;
        }
    }
}
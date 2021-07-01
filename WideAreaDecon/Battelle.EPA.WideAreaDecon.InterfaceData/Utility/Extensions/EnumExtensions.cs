using System;
using System.Runtime.Serialization;
using Microsoft.OpenApi.Extensions;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Extensions
{
    public static class EnumExtensions
    {
        public static string GetStringValue(this Enum value)
        {
            return value.GetAttributeOfType<EnumMemberAttribute>()?.Value ?? value.ToString();
        }
    }
}
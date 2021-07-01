using System;
using System.Runtime.Serialization;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter
{
    public enum PersonnelLevel
    {
        [EnumMember(Value = "OSC")] OSC,
        [EnumMember(Value = "PL-1")] PL1,
        [EnumMember(Value = "PL-2")] PL2,
        [EnumMember(Value = "PL-3")] PL3,
        [EnumMember(Value = "PL-4")] PL4
    }
}
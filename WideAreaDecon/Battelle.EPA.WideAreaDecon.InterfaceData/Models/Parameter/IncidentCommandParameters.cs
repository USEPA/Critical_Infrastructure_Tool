using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter
{
    public class IncidentCommandParameters
    {
        public Dictionary<PersonnelLevel, double> personnelReqPerTeam;
        public double personnelOverheadDays;

        public IncidentCommandParameters(
            Dictionary<PersonnelLevel, double> _personnelReqPerTeam,
            double _personnelOverheadDays)
        {
            personnelReqPerTeam = _personnelReqPerTeam;
            personnelOverheadDays = _personnelOverheadDays;
        }
    }
}

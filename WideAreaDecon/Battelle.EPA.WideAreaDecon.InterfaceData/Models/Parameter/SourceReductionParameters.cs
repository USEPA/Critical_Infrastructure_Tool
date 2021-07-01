using System.Collections.Generic;
using System.Linq;
using System;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter
{
    public class SourceReductionParameters
    {
        public double surfaceAreaToBeSourceReduced;
        public double massPerSurfaceArea;
        public double massRemovedPerHourPerTeam;
        public double numEntriesPerDay;
        public double respiratorsPerPerson;
        public double hoursEntering;
        public double hoursExiting;
        public double numTeams;
        public Dictionary<PersonnelLevel, double> personnelReqPerTeam;
        public double personnelOverheadDays;
        public Dictionary<PpeLevel, double> ppeRequired;

        public SourceReductionParameters(
            double _surfaceAreaToBeSourceReduced,
            double _massPerSurfaceArea,
            double _massRemovedPerHourPerTeam,
            double _numEntriesPerDay,
            double _respiratorsPerPerson,
            double _hoursEntering,
            double _hoursExiting,
            double _numTeams,
            Dictionary<PersonnelLevel, double> _personnelReqPerTeam,
            double _personnelOverheadDays,
            Dictionary<PpeLevel, double> _ppeRequired)
        {
            surfaceAreaToBeSourceReduced = _surfaceAreaToBeSourceReduced;
            massPerSurfaceArea = _massPerSurfaceArea;
            massRemovedPerHourPerTeam = _massRemovedPerHourPerTeam;
            numEntriesPerDay = _numEntriesPerDay;
            respiratorsPerPerson = _respiratorsPerPerson;
            hoursEntering = _hoursEntering;
            hoursExiting = _hoursExiting;
            numTeams = _numTeams;
            personnelReqPerTeam = _personnelReqPerTeam;
            personnelOverheadDays = _personnelOverheadDays;
            ppeRequired = _ppeRequired;
        }
    }
}

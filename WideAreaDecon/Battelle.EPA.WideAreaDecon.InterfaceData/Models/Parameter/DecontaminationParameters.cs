using System.Collections.Generic;
using System.Linq;
using System;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Parameter;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter
{
    public class DecontaminationParameters
    {
        public IParameter[] efficacyParameters;
        public Dictionary<SurfaceType, ApplicationMethod> applicationMethods;
        public Dictionary<SurfaceType, double> initialSporeLoading;
        public double desiredSporeThreshold;
        public Dictionary<ApplicationMethod, double> treatmentDaysPerAm;
        public Dictionary<PersonnelLevel, double> personnelReqPerTeam;
        public double personnelOverhead;
        public double numEntriesPerTeamPerDay;
        public double hoursPerEntryPerTeam;
        public double hoursPerExitPerTeam;
        public double respiratorsPerPerson;
        public double numTeams;
        public Dictionary<PpeLevel, double> ppeRequired;
        public Dictionary<SurfaceType, ContaminationInformation> areaContaminated;
        public double fumigationAgentVolume;
        public Dictionary<SurfaceType, double> agentVolume;

        public DecontaminationParameters(
            IParameter[] _efficacyParameters,
            Dictionary<SurfaceType, ApplicationMethod> _applicationMethods,
            Dictionary<SurfaceType, double> _initialSporeLoading,
            double _desiredSporeThreshold,
            Dictionary<ApplicationMethod, double> _treatmentDaysPerAm,
            Dictionary<PersonnelLevel, double> _personnelReqPerTeam,
            double _personnelOverhead,
            double _numEntriesPerTeamPerDay,
            double _hoursPerEntryPerTeam,
            double _hoursPerExitPerTeam,
            double _respiratorsPerPerson,
            double _numTeams,
            Dictionary<PpeLevel, double> _ppeRequired,
            Dictionary<SurfaceType, ContaminationInformation> _areaContaminated,
            double _fumigationAgentVolume,
            Dictionary<SurfaceType, double> _agentVolume)
        {
            efficacyParameters = _efficacyParameters;
            applicationMethods = _applicationMethods;
            initialSporeLoading = _initialSporeLoading;
            treatmentDaysPerAm = _treatmentDaysPerAm;
            agentVolume = _agentVolume;
            desiredSporeThreshold = _desiredSporeThreshold;
            personnelReqPerTeam = _personnelReqPerTeam;
            personnelOverhead = _personnelOverhead;
            numEntriesPerTeamPerDay = _numEntriesPerTeamPerDay;
            hoursPerEntryPerTeam = _hoursPerEntryPerTeam;
            hoursPerExitPerTeam = _hoursPerExitPerTeam;
            respiratorsPerPerson = _respiratorsPerPerson;
            numTeams = _numTeams;
            ppeRequired = _ppeRequired;
            areaContaminated = _areaContaminated;
            fumigationAgentVolume = _fumigationAgentVolume;
        }
    }
}

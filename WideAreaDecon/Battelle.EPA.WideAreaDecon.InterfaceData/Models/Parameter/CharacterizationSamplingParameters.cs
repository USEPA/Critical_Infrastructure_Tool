using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter
{
    public class CharacterizationSamplingParameters
    {
        public double fractionSampledWipe;
        public double fractionSampledHepa;
        public double surfaceAreaPerWipe;
        public double surfaceAreaPerHepa;
        public double wipesPerHrPerTeam;
        public double hepaSocksPerHrPerTeam;
        public double numTeams;
        public double samplePackageTime;
        public int numLabs;
        public List<double> labUptimesHours;
        public List<double> labDistanceFromSite;
        public List<double> labThroughput;
        public double resultTransmissionToIC;
        public Dictionary<PersonnelLevel, double> personnelReqPerTeam;
        public double personnelOverheadDays;
        public double entriesPerTeam;
        public double hoursEntering;
        public double hoursExiting;
        public double respiratorsPerPerson;
        public Dictionary<PpeLevel, double> ppeRequired;

        public CharacterizationSamplingParameters(
            double _fractionSampledWipe,
            double _fractionSampledHepa,
            double _surfaceAreaPerWipe,
            double _surfaceAreaPerHepa,
            double _wipesPerHrPerTeam,
            double _hepaSocksPerHrPerTeam,
            double _numTeams,
            double _samplePackageTime,
            int _numLabs,
            List<double> _labUptimeHours,
            List<double> _labDistanceFromSite,
            List<double> _labThroughput,
            double _resultTransmissionToIC,
            Dictionary<PersonnelLevel, double> _personnelPerTeam,
            double _personnelOverheadDays,
            double _entriesPerTeam,
            double _hoursEntering,
            double _hoursExiting,
            double _respiratorsPerPerson,
            Dictionary<PpeLevel, double> _ppeRequired)
        {
            fractionSampledWipe = _fractionSampledWipe;
            fractionSampledHepa = _fractionSampledHepa;
            surfaceAreaPerWipe = _surfaceAreaPerWipe;
            surfaceAreaPerHepa = _surfaceAreaPerHepa;
            wipesPerHrPerTeam = _wipesPerHrPerTeam;
            hepaSocksPerHrPerTeam = _hepaSocksPerHrPerTeam;
            numTeams = _numTeams;
            samplePackageTime = _samplePackageTime;
            numLabs = _numLabs;
            labUptimesHours = _labUptimeHours;
            labDistanceFromSite = _labDistanceFromSite;
            labThroughput = _labThroughput;
            resultTransmissionToIC = _resultTransmissionToIC;
            personnelReqPerTeam = _personnelPerTeam;
            personnelOverheadDays = _personnelOverheadDays;
            entriesPerTeam = _entriesPerTeam;
            hoursEntering = _hoursEntering;
            hoursExiting = _hoursExiting;
            respiratorsPerPerson = _respiratorsPerPerson;
            ppeRequired = _ppeRequired;
        }
    }
}

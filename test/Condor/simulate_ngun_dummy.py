import FWCore.ParameterSet.Config as cms

process = cms.Process('SIM')

# import of standard configurations
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
#process.load('Geometry.CMSCommonData.cmsExtendedGeometryXML_cfi')
#process.load('SimG4CMS.Forward.zdcGeometryXML_cfi')
process.load("Geometry.ForwardCommonData.zdcGeometry_cfi")
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration/StandardSequences/Generator_cff')
process.load('Configuration/StandardSequences/VtxSmearedNoSmear_cff')
process.load('Configuration/StandardSequences/Sim_cff')
process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load('Configuration/EventContent/EventContent_cff')
process.load('Configuration.Geometry.GeometryExtended2016_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(200)
)

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')


# Input source
process.source = cms.Source("EmptySource")

process.generator = cms.EDProducer("FlatRandomEGunProducer",
    PGunParameters = cms.PSet(
        PartID = cms.vint32(2112),
        MinEta = cms.double(10.0),
        MaxEta = cms.double(20.0),
        MinPhi = cms.double(-3.14159265359), ## in radians
        MaxPhi = cms.double(3.14159265359),
        MinE = cms.double(2559.99),
        MaxE = cms.double(2561.01)
    ),
    Verbosity = cms.untracked.int32(0), ## set to 1 (or greater)  for printouts

    psethack = cms.string('single neutron E 100'),
    AddAntiParticle = cms.bool(False),
    firstRun = cms.untracked.uint32(1)
)

process.ProductionFilterSequence = cms.Sequence(process.generator)

# Output definition
process.output = cms.OutputModule("PoolOutputModule",
    outputCommands = process.FEVTDEBUGEventContent.outputCommands,
    fileName = cms.untracked.string('simevent.root'),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM'),
        filterName = cms.untracked.string('')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Special settings
process.g4SimHits.UseMagneticField = cms.bool(False)
process.g4SimHits.Physics.DefaultCutValue = cms.double(10.)
process.g4SimHits.Generator.HepMCProductLabel = 'LHCTransport'
process.g4SimHits.Generator.MinEtaCut = cms.double(-9.0)
process.g4SimHits.Generator.MaxEtaCut =  cms.double(20.0)
'''process.g4SimHits.Watchers = cms.VPSet(cms.PSet(
    type = cms.string('ZdcTestAnalysis'),
    ZdcTestAnalysis = cms.PSet(
        Verbosity = cms.int32(0),
		StepNtupleFlag = cms.int32(0),
        EventNtupleFlag = cms.int32(0),
        StepNtupleFileName = cms.string('stepNtuple.root'),
        EventNtupleFileName = cms.string('eventNtuple.root')
	)
))'''
process.g4SimHits.ZdcSD.UseShowerLibrary = cms.bool(False)
process.g4SimHits.ZdcSD.UseShowerHits = cms.bool(True)
process.RandomNumberGeneratorService.generator.initialSeed = cms.untracked.uint32(SEED)
#process.g4SimHits.StackingAction.MaxTrackTime = cms.double(100000.)
#process.g4SimHits.CaloSD.TmaxHit = cms.double(100000.)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('OUTPUT')
)

process.analyzer = cms.EDAnalyzer('zdcSimAnalyzer'
     ,simhits = cms.InputTag("g4SimHits","ZDCHITS","SIM")
)

# Path and EndPath definitions
process.generation_step = cms.Path(process.ProductionFilterSequence+process.pgen)
process.simulation_step = cms.Path(process.psim)
process.endjob_step = cms.Path(process.endOfProcess)
#process.out_step = cms.EndPath(process.output)
process.analyzer_step = cms.Path(process.analyzer)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.simulation_step,process.endjob_step,process.analyzer_step)

def customise(process):
    #Adding SimpleMemoryCheck service:
    process.SimpleMemoryCheck=cms.Service("SimpleMemoryCheck",
                                          ignoreTotal=cms.untracked.int32(1),
                                          oncePerEventMode=cms.untracked.bool(True))
    #Adding Timing service:
    process.Timing=cms.Service("Timing")

    #Tweak Message logger to dump G4cout and G4cerr messages in G4msg.log
    #print process.MessageLogger.__dict__
    process.MessageLogger.destinations=cms.untracked.vstring('cout'
                                                             ,'cerr'
                                                             #,'G4msg'
                                                             )
    process.MessageLogger.categories=cms.untracked.vstring('FwkJob'
                                                           ,'FwkReport'
                                                           ,'FwkSummary'
                                                           #,'Root_NoDictionary'
                                                           #,'TimeReport'
                                                           #,'TimeModule'
                                                           #,'TimeEvent'
                                                           #,'MemoryCheck'
                                                           #,'PhysicsList'
                                                           #,'G4cout'
                                                           #,'G4cerr'
                                                           #,'CaloSim'
                                                           #,'ForwardSim'
    )

    process.MessageLogger.debugModules=cms.untracked.vstring('g4SimHits')

    #Configuring the G4msg.log output
    '''process.MessageLogger.G4msg =  cms.untracked.PSet(
        noTimeStamps = cms.untracked.bool(True)
        #First eliminate unneeded output
        ,threshold = cms.untracked.string('INFO')
        ,INFO = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,DEBUG = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,FwkReport = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,FwkSummary = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,Root_NoDictionary = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,FwkJob = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,TimeReport = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,TimeModule = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,TimeEvent = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,MemoryCheck = cms.untracked.PSet(limit = cms.untracked.int32(0))
        #TimeModule, TimeEvent, TimeReport are written to LogAsbolute instead of LogInfo with a category
        #so they cannot be eliminated from any destination (!) unless one uses the summaryOnly option
        #in the Timing Service... at the price of silencing the output needed for the TimingReport profiling
        #
        #Then add the wanted ones:
        ,PhysicsList = cms.untracked.PSet(limit = cms.untracked.int32(-1))
        ,G4cout = cms.untracked.PSet(limit = cms.untracked.int32(-1))
        ,G4cerr = cms.untracked.PSet(limit = cms.untracked.int32(-1))
        ,CaloSim = cms.untracked.PSet(limit = cms.untracked.int32(-1))
        ,ForwardSim = cms.untracked.PSet(limit = cms.untracked.int32(-1))
        )'''

    #Add these 3 lines to put back the summary for timing information at the end of the logfile
    #(needed for TimeReport report)
    process.options = cms.untracked.PSet(
        wantSummary = cms.untracked.bool(True)
        )

#    process.g4SimHits.G4Commands = cms.vstring('/tracking/verbose 1')

    return(process)

# End of customisation function definition

process = customise(process)

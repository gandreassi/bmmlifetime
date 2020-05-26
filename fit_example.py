import ROOT as r

#import data in ROOT format
c = r.TChain("Candidates")
c.Add("/mnt/hadoop/scratch/gandreas/NanoAOD/505/BuToJpsiK_BMuonFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen+RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2+MINIAODSIM/MCmatch_flat_Bukmm/*.root")
#apply a cut
cut =   "HLT_DoubleMu4_3_Jpsi && "\
        "bkmm_kaon_pt>2 && abs(bkmm_kaon_eta)<1.4 && "\
        "bkmm_jpsimc_sl3d>4 && "\
        "abs(Muon1_eta)<1.4 && abs(Muon2_eta)<1.4 && "\
        "Muon1_pt>4 && Muon2_pt>4 && "\
        "Muon1_softId==1 && Muon2_softId==1 && "\
        "bkmm_jpsimc_vtx_chi2dof<5"
c = c.CopyTree(cut)

#define variables
B_mass = r.RooRealVar("bkmm_jpsimc_mass", "bkmm_kin_mass", 5.0,5.7) #reconstructed B mass
tau_gen = r.RooRealVar("mm_gen_tau", "mm_gen_tau", 0, 15) #generated decay time
tau_meas = r.RooRealVar("mm_kin_tau", "mm_kin_tau", 0, 15) #reconstructed decay time
tau_meas_e = r.RooRealVar("mm_kin_taue", "mm_kin_taue", 0, 5) #uncertainty on reconstructed decay time

#import dataset
rds = r.RooDataSet("rds", "rds", c, r.RooArgSet(B_mass, tau_gen, tau_meas, tau_meas_e))
print ("Dataset contains {0} events.".format(rds.sumEntries()))

#mass model
B_mass_mean = r.RooRealVar("B_mass_mean", "#mu", 5.28, 5.25, 5.3)
B_mass_sigma1 = r.RooRealVar("B_mass_sigma1", "#sigma_{1}", 0.01,0.005,0.05)
B_mass_sigma2 = r.RooRealVar("B_mass_sigma2", "#sigma_{2}", 0.04,0.005,0.05)
B_mass_sigma3 = r.RooRealVar("B_mass_sigma3", "#sigma_{3}", 0.1,0.05,0.5)

mg1 = r.RooGaussian("g1", "g1", B_mass, B_mass_mean, B_mass_sigma1)
mg2 = r.RooGaussian("g2", "g2", B_mass, B_mass_mean, B_mass_sigma2)
mg3 = r.RooGaussian("g3", "g3", B_mass, B_mass_mean, B_mass_sigma3)

m_gfrac1 = r.RooRealVar("f1", "f1", 0.6, .2, .9) #fraction of integral taken by the first gaussian
m_gfrac2 = r.RooRealVar("f2", "f2", 0.3, .0, .8) #fraction of integral taken by the second gaussian

#sum up the three gaussians
signal_model = r.RooAddPdf("signal_model", "signal_model", r.RooArgList(mg1,mg2,mg3), r.RooArgList(m_gfrac1,m_gfrac2))

#fit model to data
signal_model.fitTo(rds)

#plot data and model on a new canvas
frame = B_mass.frame()
rds.plotOn(frame)
signal_model.plotOn(frame)
c = r.TCanvas("c")
frame.Draw()
c.Draw()

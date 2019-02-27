#ifndef CATTools_CommonTools_TTbarModeDefs_H
#define CATTools_CommonTools_TTbarModeDefs_H

namespace TZWi
{

enum TTChannel { CH_NOTT = -1, CH_FULLHADRON = 0, CH_SEMILEPTON, CH_FULLLEPTON, CH_MULTILEPTON };
enum WMode { CH_HADRON = 0, CH_MUON, CH_ELECTRON, CH_MUONELECTRON,
             CH_TAU_HADRON, CH_TAU_MUON, CH_TAU_ELECTRON, CH_TAU_MUONELECTRON};

};

#endif


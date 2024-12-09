from django.core.management.base import BaseCommand
from floorsheet.models import Sector

class Command(BaseCommand):
    help = 'Populate Sector model with initial data'

    def handle(self, *args, **kwargs):
        sectors = [
            (1, 'Commercial Banks', 'NABIL, NIMB, SCB, HBL, SBI, NBB, EBL, BOKL, NICA, MBL, LSL, KBL, LUBL, NCCB, SBL, GRAND, SANIMA, NMB, PRVU, EBLCP, GBIME, CZBIL, BOAN, PCBL, SRBL, ADBL, JBNL, NBL, SIGS1, CBL, NBF1, CTBNL, MEGA, CCBL, SEOS, NMBSF1, NIBSF1, LVF1, SBLD78, GIMES1, NMBHF1, NE'),
(2, 'Hotels', 'YHL, SHL, TRH, OHL, TRHPR, CGH, KDL, CITY'),
(3, 'Others', 'ESC, NFD, NTC, NRIC, NRM, MKCL, NWCL, HRL'),
(4, 'Hydro Power', 'NHPC, BPCL, CHCL, AHPC, SHPC, RIDI, BARUN, API, NGPL, KKHC, DHPL, AKPL, SPDL, UMHL, CHL, HPPL, NHDL, RADHI, RRHP, PMHPL, KPCL, AKJCL, JOSHI, UPPER, GHL, UPCL, MHNL, PPCL, HURJA, UNHPL, RHPL, SJCL, HDHPC, LEC, SSHL, MEN, UMRH, GLH, SHEL, RURU, MKJC, SAHAS,'),
(5, 'Tradings', 'STC, BBC, NBCK, NTL, NWC'),
(6, 'Development Banks', 'NIDC, NDB, PDBL, GDBL1, BUDBL, SDBL, BBBL, NABBC, BBBLN, SBBLJ, GDBNL, KBBL, ACEDBL, APEX, SUPRME, SODBL, EDBL, MLBL1, BLDBL, IDBL, PRBBL, DBBL, SUBBL, CEDBL, TBBL, PGBL, REDBL, AXIS, LBBL, MGBL, PDB, MBBL, MDB, PBSL, RBSL, KDBL, SEWA, NGBL, ODBL, MLBL, U'),
(7, 'Microfinance', 'NUBL, CBBL, DDBL, SWBBL, NLBBL, FMDBL, SMFDB, SLBBL, SKBBL, RMDC, GBLBS, NSLB, KMCDB, MLBBL, NBBL, LLBS, MMFDB, VLBS, MSMBS, HLBSL, KLBSL, JSLBB, NMBMF, GILB, SWMF, MERO, NMFBS, RSDC, SLBS, FOWAD, SMATA, SDESI, MSLB, SMB, USLB, AMFI, WNLB, NADEP, ACLBSL, '),
(8, 'Non Life Insurance', 'NICL, RBCL, HEI, UAIL, EIC, SPIL, NIL, PRIN, SALICO, IGI, PICL, LGIL, SICL, SIL, NLG, AIL, GIC, SGIC'),
(9, 'Life Insurance', 'NLICL, NLIC, LICN, ALICL, HLI, SJLIC, GLICL, RLI, PMLI, JLI, ULI, SRLI, ILI, RNLI, SNLI, CLI'),
(10, 'Manufacturing And Processing', 'MSM, BNL, BJM, NLO, NVG, RJM, BSM, GRU, JSM, AVU, BNT, HBT, BSL, UNL, NKU, HTL, SBPP, FHL, SRS, NBBU, HDL, SHIVM, GCIL, SONA'),
(11, 'Finance', 'NFS, NCM, NNFC, NSM, GUFL, PFCL, UFCL, NABB, NFL, YFL, GFLK, SFC, UFLK, NHMF, BFC, MFL, LFC, GFCL, PFC, PFL, LFLC, SFL, AEFL, NBFL, UFL, ILFC, SIFC, CFCL, NSLMB, PFCLL, NDFL, SYFL, JFL, STFL, OFL, CMBF, FFCL, SFCL, BJFL, EFL, CMB, PFIL, SFFIL, GMFIL, IMEF')
            # Add more sectors as needed...
        ]

        for sector_id, name, symbols in sectors:
            sector, created = Sector.objects.get_or_create(
                id=sector_id,
                defaults={'name': name, 'symbols': symbols}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Sector '{name}' created successfully."))
            else:
                self.stdout.write(self.style.WARNING(f"Sector '{name}' already exists."))

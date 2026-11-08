from pathlib import Path
import json,hashlib
B=Path(__file__).parent
baseq=json.loads((B/'seed-v2/questions.json').read_text());basek=json.loads((B/'seed-v2/answer-key.json').read_text());questions=list(baseq['questions']);answers=list(basek['answers']);novel=[]
def add(q,a,f,refs,why):
 i=f'Q{len(questions)+1:02d}';questions.append({'id':i,'question':q});answers.append({'id':i,'expected_answer':a,'required_facts':f,'contextual_background':[],'source_refs':refs});novel.append({'id':i,'decision':'accepted','novelty':why,'source_refs':refs})
add('What is the per-district limit for androids, developments, illnesses, outages, prisec, Human First and orgcrime? Can Human First and orgcrime coexist, which duplicate incoming components move, and may the spare fourth android be added to play?',
'At most1 of each named type per district. Different enemy types may coexist without prisec. Incoming duplicate enemy/illness/outage moves; development/unrest never move and android may not enter occupied android district. Fourth android is a replacement spare, not additional productive android.',
['one each of all7 named types','different enemies can coexist absent prisec','duplicate enemy illness outage move; android not into occupied android; development/unrest never move','fourth android spare only'],['RR5.3,19.4,31.2,32.3,35.3–35.5,38.1,39.3,42.3; FAQ Other'],'Per-type capacity and spare component scope were not actually asked by seed; component-shortage and relocation questions do not ask all limits.')
add('A corporation has44 capital, then loses7. Where and which side is its capital token before and after? Do the bright multiples-of-five spaces award anything?',
'At44 use40-side at4. After losing7 total37, normal-side at37. Bright multiples5 confer no effect.',
['44 means40-side4','37 means normal-side37','bright multiples5 no effect'],['RR7.2–7.6'],'Unasked capital wrap/down-crossing and visual-space branch.')
add('With Braintrust, what does four-player Globalsec draw and what is its hand limit? What does Melange draw, and may its doubled General cards all come from one type?',
'Globalsec4security then2General from a single nonsecurity type, hand4. Melange2General then2General then2General, three distinct types, two cards from each. Braintrust doubles each entry and reduces hand limit1.',
['Globalsec4security then2 same-type General excludingsecurity','hand4','Melange3entries of2 each different decks; not all6one type'],['Printed asset3 Braintrust; corporation back0/both3; RR3.1,29,30'],'Persistent sheet multiplier with separate General entries and modified hand limit.')
add('What changes when Floyd2X3A7C is claimed, and what is a normal player’s hand limit while owning it? If Floyd is gained by trade instead, is the five-card draw repeated and does the hand limit benefit apply?',
'Claim draws5actions of any types. Ownership adds5hand size, normally10. Trade does not claim so no draw; hand-size benefit applies while owned.',
['claim5actions anytypes','normalhand10 whileowned','trade no redraw but handbenefit applies'],['Printed asset11; RR6,9,30'],'Distinguishes claim-only draw from continuous ownership hand modification.')
add('What does Toshiyuki Sakai do when claimed, how many actions are drawn in total, and is the hand-size exception permanent?',
'Discard him onclaim to draw2each of5types=10actions. Do not discard down to handsize this turn; it is a turn-specific exemption, not permanent increased limit.',
['discardonclaim','2eachfive=10','no discardtohandlimit thisturn only notpermanent'],['Printed asset32; RR2.3,9,30'],'Temporary hand-limit bypass differs from persistent Floyd/Braintrust modifications.')
add('At the start of another player’s turn, they have12 capital and Lily Lockwell’s owner has10. What may Lily do, is the stolen card random, when relative to Refresh, and what if both have10?',
'Owner may steal1random handaction before Refresh. At equal10 the more-capital condition fails so no steal.',
['optional1randomhandaction','beforeRefresh','12>10qualifies equal10doesnot'],['Printed asset17; RR6.6,56.3'],'Start-of-turn conditional private/random theft and before-Refresh timing.')
add('When may Rachel Beckmann draw, including during another player’s deal, what hand condition and card type apply, and does a faceup emergency stop it?',
'At end of eachdeal if hand0 maydraw1action of topmost sheettype. Not limited to ownturn. Emergencyoutsidehand doesnotprevent0condition.',
['eachdealend includingotherturn','0hand optional1topmosttype','emergencydoesnotcount'],['Printed asset26; RR21.4,30.1'],'Every-deal empty-hand trigger distinct from own End of Turn.')
add('Aaron Marrón’s owner proposes the third counteroffer; another player later proposes the fourth. How many extra cards are paid for each, where do those paid cards go, and does Aaron intercept support-card discards?',
'Owner pays2extra toshared facedowndiscard as usual because Aaron onlyanotherplayer. Fourthproposer pays3cards toAaronowner insteadofdiscard. Aarononlycounterofferproposal costs, notsupport cleanup.',
['thirdowner2normaldiscard','fourthanother3toAaronowner','notarbitrary/supportdiscards'],['Printed asset0; RR15.4,16.5'],'Redirected discard destination with other-player restriction; escalating counts are application of seed rule.')
add('A supporting player abstains. When and at what cost can Eiko respond, and what choices must that player then make?',
'At abstention owner may exhaust Eiko; abstainer mustplay1card supportingmain offer orlose1capital.',
['whenabstainsduringSupport','optionalexhaustEiko','abstainer1main-supportcardorlose1capital'],['Printed asset8'],'Abstention-triggered forced support/penalty exception.')
add('How does The Fall Guy allow an active player to make a counteroffer, what is discarded, what step follows immediately, and can Chief Gorman cancel that counteroffer?',
'Afterownmain offer maydiscardFallGuy toproposecounteroffer too. ProceedimmediatelySupport, noothercounterofferopportunities; Chiefcannotcancel thiscounteroffer.',
['afterownmain optionaldiscardasset','activecounterofferpermitted','immediateSupport skipsotherscounterchance','Chiefcannotcancel'],['Printed asset10; FAQ The Fall Guy'],'Explicit active-counteroffer exception and immediate timing lockout.')
add('When may Chief Gorman be used on an ordinary counteroffer, what payment avoids its return, and what happens to the proposer’s status, further counteroffers and already-paid proposal discards if returned?',
'Afterproposal owner mayexhaustChief unlessproposergivesowner2capital. Returnedoffergoesproposerhand; losescurrentcounteringstatus,cannotcounteragainthatturn; proposalcostdiscardsnotrefunded.',
['aftercounterproposal optionalexhaust','2capitalpaidtoChiefowner avoidsreturn','returnhand endsstatus noanothercounterthisturn','proposaldiscardsnotrefunded'],['Printed asset6; RR15.8'],'Ordinary counteroffer cancellation and its sunk-cost/status consequences.')
add('For an ordinary offered action other than Unorthodox Knowledge, when and at what cost may Caprice Nisei act, and is the proposer then free to change the announced resolution?',
'Whenplayerproposesoffer owner mayexhaustCaprice; proposer mustdeclareexactlyhowitwillresolve andisbound, cannotfreelychange.',
['whenofferproposed optionalexhaust','exactdeclarationrequired andbinding'],['Printed asset5; RR2.9'],'Positive binding-declaration branch, beyond seed Unorthodox exemption.')
add('At the start of Support, Isabel McGuire’s owner puts a deck card beside the counteroffer. Is the owner treated as supporting that offer, may an eligible owner then support the main offer normally, and does Locust Company’s restriction on that owner block Isabel’s deck card?',
'OptionalexhaustIsabel atstartSupport places1topcardofanyactiondeck insupporteither. Doesnotmakeownerasupporterofchosenoffer. Ifeligible maynormal-supporteitherinclmain. Locustblocks handcounteroffersupport, notdeckviaIsabel.',
['startSupport optionalexhaust1topanyactiondecktoeitheroffer','notcountedasowner-supportingchosenoffer','eligibleownnormalmaymaineither','Locusthandrestrictiondoesnotblockdeck'],['Printed assets15,18; FAQ Isabel/Locust'],'Official deck-support versus player-support identity exception and Locust source restriction.')
add('When and at what cost does Locust Company restrict a player, which offer/card source is restricted, and may that player still support the main offer from hand?',
'AtstartSupport owner mayexhaustLocust chooseplayer. Chosenplayercannotplayhandcards supportingcounteroffer; mainsupportfromhandallowed.',
['startSupportoptionalexhaustchooseplayer','counterofferfromhandonlyblocked','mainfromhandlegal'],['Printed asset18; FAQ Locust'],'Positive restricted/unrestricted hand-support branches complement Isabel exception.')
add('When are Midori and Tanaka used, what cost does each have, and which one requires a support tie? What winners may each choose?',
'Midori whendeterminingwinnerduringResolution, mayexhaust iftied, decidedealwinner(activeorcountering). Tanaka atstartResolution maydiscard chooseactiveorcounteringwinner withouttienecessary.',
['Midoriduringwinnerdetermination optionalexhaust tieonly','TanakastartResolution optionaldiscard notie','chooseactiveorcounteringwinner'],['Printed assets21,30; RR6.4'],'Distinct winner-override timing, costs and tie condition.')
add('After a player proposes an offer, what may Mark Yale do, who becomes unable to trade, what kinds of trades are blocked, and for how long?',
'Owner mayexhaustMark afteroffer; thatproposer cannottradecapital/assets untildealend. Otherplayersnotgenerallyblocked.',
['afterofferoptionalexhaust','onlyproposer','capital/assetsuntildealend','othersnotblocked'],['Printed asset20'],'Per-player trading lockout as card exception to anytime trading.')
add('When using Naoko Watanabe, what is discarded and what is claimed? If the first gained asset has a when-claimed effect, does it wait until after the second claim?',
'OnNaokoclaim discardhertoclaimtop2assetsoneatatime. Firstwhenclaimed effectresolvesbeforesecondclaim.',
['discardNaokoonclaim','top2assetsclaimedsequentially','firstclaimtriggerbeforesecond'],['Printed asset25; FAQ Naoko'],'Sequential claim timing exception explicitly required by FAQ.')
add('Sunny LeBeau is present when one effect increases threat by3, and later an event sends two orgcrime units into the Root in separate instances. How many times can Sunny trigger in each case, what may be drawn each time, and does an exhaust cost apply?',
'One+3instance triggersSunnyonce. TwoRootentriestrigger twice, onceeach. Eachoptionaltriggerdraws2actions topmostsheettype, noexhaustcostprinted.',
['single+3one trigger','twoRootentries2triggers','optional2topmosttypeeach','noexhaustcost'],['Printed asset28; FAQ Sunny'],'Per-instance versus per-point trigger with official repeated-Root example.')
add('What threat increases trigger Wong Ya Ching and how much capital does it award? Does ordinary demand failure or an orgcrime moving to the Root qualify merely because it increases threat?',
'Illnesstoken effectincreasingthreat gives2capital. Genericdemand ororgcrimeRoot isnotillnesstoken effectanddoesnotqualify.',
['illnesstokeneffectthreat2capital','demandno','orgcrimeRootno'],['Printed asset33; RR32,63'],'Trigger source restriction distinguishes illness income from all-threat Sunny.')
add('Describe Elizabeth Mills’s End of Turn ownership change and who chooses its following effect. What are the two effects, and which action type is used for the draw?',
'GiveMillstoanotherplayerfirst; currentuserchoosesrecipientmustdiscard3actions or draw3oftopmosttypeonrecipientssheet.',
['EndofTurngiveanotherfirst','usernotrecipientchooses','discard3ordraw3recipienttopmosttype'],['Printed asset9'],'Transfer-before-effect timing and chooser/recipient distinction.')
add('What does Susan Chen do at End of Turn and in what order? If the active player receives her during their End of Turn step, can they use her that turn?',
'Gain2capital then giveSusantoanotherplayer. IfreceivedduringactiveownEndofTurncanusethatturn undergeneralnewasset rule.',
['gain2beforetransferanother','receivedinownEndstepusablethen'],['Printed asset29; RR22.4'],'Capital-before-transfer order plus newly enabled end-step use.')
add('With Alex Westlund, what cards can be swapped, when is the capital cost paid if one selected asset is yours, can Alex himself be selected, and do those assets count as claimed?',
'EndofTurnchoose2inplayassets; ifanyownlose2before swap,canincludeAlex; swapsnotclaims.',
['EndofTurn2inplayassets','anyowncost2before','Alexselfallowed','notclaimed'],['Printed asset1; RR61.1'],'Asset swap cost timing and self-selection explicitly clarified by RR.')
add('What may Bernice Mai do at End of Turn, how is capital calculated, and can this ability give emergency actions despite the prohibition on freely trading hand actions?',
'Giveupto2handactionstoanotherplayer, gain1capitalpergiven. Explicitabilitycantransferhandactions despiteordinarytradeban; emergenciesoutsidehand cannotbegivenbyit.',
['EndofTurnupto2handcardsanother','capitalcountgiven','explicitabilitytransfernotordinarytrade','emergencyoutsidehandexcluded'],['Printed asset2; RR21.4,65.5 corrected'],'Explicit hand-card transfer versus ordinary trade ban; outside-hand scope.')
add('Fumiko Yamamori is used at End of Turn. What resource condition and payment apply, how much capital is gained, and can a resource at0 be chosen for free income?',
'Chooseone nonzero supplyresource, reduce1togain2capital; zero cannotbechosen.',
['EndofTurnone nonzeroresource','reduce1togain2capital','zeroillegal'],['Printed asset12; RR58.3'],'Positive nonzero resource cost gates personal capital payout.')
add('Marco Cubrero is used when two other players tie for most capital. What are the one-capital and two-capital options, and must the richer target be unique?',
'EndofTurnsteal1fromanyplayer or2fromoneoftiedrichestplayers chosenbyuser; uniquenessnotrequired.',
['EndofTurn1anyor2richest','chooseoneoftiedrichest'],['Printed asset19'],'Explicit tied-richest target branch; not a cosmetic change to normal theft.')
add('When using Jackson Howard, when is the prediction made, what cost applies, can you choose yourself, and what produces the capital payment?',
'Whenassetrevealed mayexhaustchooseanotherplayer; cannotself; ifchosenwinsdealgain2capital.',
['assetrevealedbeforeoutcome optionalexhaust','anothernotself','chosenwins2capital'],['Printed asset16'],'Reveal-time prediction/payment and other-player restriction.')
add('Whose deal victory pays Coach Walden? When may Monica Singh steal, and who is the target? When Saul Eustecio is used, which player wins the deal and who gains capital in what order?',
'Coachpays1whenrightneighborwins. Monicaownerlosingasactive maysteal2fromcounterer. Saulwhencountererwins mayexhaust; ownusergains1thenactivegains1.',
['Coachrightneighborwin1','Monicaownactive-loss optionalsteal2counterer','Saulcountererwin optionalexhaust','Sauluser1thenactive1'],['Printed assets7,22,27'],'Actor-restricted win/loss income triggers and Saul ordered two-recipient effect.')
add('At End of Turn, how do Mr. Li and Mr. White differ in targeting, capital change, drawing versus inspecting/stealing, and who can be chosen?',
'MrLi chooseanyplayer loses1capital draws2actionsanytypes. MrWhite lookatanotherplayershand maysteal1ofthoseactions; noLi-likecapital/draweffect.',
['LiEndanyplayer loses1draws2anytypes','WhiteEndanother privatehandlook optionalsteal1'],['Printed assets23,24; RR56.3'],'Different targeting/privacy operations; MrWhite explicit private inspection exception.')
add('What does Hernando Cortez do on being claimed, and if he steals an exhausted asset, does that asset ready or trigger its when-claimed ability? What alternative is available?',
'DiscardHernandoonclaimtosteal1assetfromanotherplayer orgain2capital. Stolenassetstaysexhaustedandisnotclaimedso no claimtrigger.',
['discardonclaim steal1anotherassetor2capital','stolenexhaustedstays','notclaimnotrigger'],['Printed asset14; RR9.1,26.2,56.2'],'On-claim choice between theft and payment; theft destination/status applies existing general rule.')
add('Describe every emergency action’s printed effect in order, including quantities, later consequences, who chooses Energy for All’s types, and any illness exception.',
'Globalsecremoveupto4enemies thenunrest+1in2districtsnotstrike/outage. Haaschooseupto2resources+1each thengain4andplace2HumanFirst. Jintekiremoveupto4illness thenplace2outages; illnessimmune. Melangeeachplayerdraw4oneownchosentype activeclockwise then+1threat. NBNreduceupto4totalunreststagesacrossdistricts thenplace2illness; noimmunity. Weylandremoveupto3outages thenplace2orgcrime.',
['Globalsecupto4enemy then+1unrestin2legal districts','Haasupto2types+1each thengain4and2HumanFirst','Jintekiupto4illness then2outage illnessimmune','Melangeeach4oneownchosentype activeclockwise then+1threat','NBNupto4totalstages then2illness noimmunity','Weylandupto3outages then2orgcrime'],['Printed emergencyfaces0–5'],'Seed tests emergency lifecycle only; this tests complete meaningful distinct emergency procedures without duplicate copies.')
add('Labor Solutions is resolved with multiple androids. How many may move, can two occupied android districts simply swap simultaneously, what later component is placed, and is illness waived?',
'Upto3androids move sequentiallytolocationswithoutandroids, nodirectsimultaneousoccupiedswap; thenplace1orgcrimeanydistrict. Noillnessexemption.',
['upto3sequentialunoccupieddestinations nosimultaneousswap','then1orgcrime','noillnesswaiver'],['Printed Laborcells10–14; RR5.2,32'],'Multi-relocation timing before mandatory enemy placement; distinct from illness-exempt single move.')
add('How does Efficiency Experts move an android and treat illness? Contrast its illness handling with a normal action involving an ill departure/destination.',
'Move1androidtoanydistrictwithoutandroid ignoringpaths. Printedillnessimmunity means noillnesseffectthreat; normalillactionwould+2total.',
['1androidunoccupiedanydistrict','explicitillnessimmunity','normalinvolvedillness+2'],['Printed Labor0–4; RR5,32'],'Specific action immunity distinguishes otherwise identical android relocation.')
add('Liquidation targets a district with Human First, orgcrime, development, primary2credits and secondary1entertainment, currently stable. State its produced resources and final unrest, and whether Human First’s exploitation outage rule applies.',
'Produces3credits and1entertainment; orgcrimeexplicitlyignoredanddevelopmentadds1. Thenunrestsetstrike. Notexploitation, soHumanFirstexploitationincrease/outage ruledoesnotapply.',
['3credits1entertainment','orgcrimeignoreddevelopmentapplies','finalstrikeexplicit','noHumanFirstexploitationoutage'],['Printed Labor15–19; FAQ Liquidation; RR43'],'New consequential Liquidation/HumanFirst non-exploitation branch and explicit strike; seed asks modifier classification without this interaction.')
add('High-Risk Investments selects three players. How does the selection order affect their capital, and does the offer’s resolver have to be one of those recipients?',
'Firstchosen3capital,second2,third1. Cardchooses3playerswithoutrequiringresolveramongthem; legalchosenplayersdeterminethegrants.',
['ordered3,2,1capital','noresolver-recipientrequirement'],['Printed Labor5–9'],'Ordered recipient selection is the rule, rather than numerical substitution in an existing grant.')
add('For Puff Piece, who chooses card types, what is the draw amount for someone who supported the winning offer versus someone who did not, is drawing optional, and in what order?',
'Eachplayer maydrawownchosentype2actions,or3ifsupportedthisoffer; activeclockwise. Supportingoppositeofferdoesnotqualify.',
['eachmaychooseoneowntype','3supportedthisoffer otherwise2','activeclockwise','oppositesupportnotqualify'],['Printed Media10–14'],'Support-dependent benefit and per-player optional same-type draw procedure.')
add('Spin Doctors resolves when supply credits are0. What unrest changes are available, what replaces the credit reduction, and what if credits instead started at1?',
'Decrease1stageinupto2districts. At0creditadd1threatinstead; at1reducecreditto0andnoalternative+1threat.',
['upto2districts1stagedecrease','0credits+1threatinstead','1creditsgo0withoutalternative+1'],['Printed Media15–19'],'Explicit zero-supply substitution versus ordinary successful cost branch.')
add('Media Circus is resolved in a district in strike. What happens to that unrest and what later unit must be placed? For24/7 Live Feeds, what alternative effect can be chosen instead of decreasing unrest?',
'MediaCircusdecreases2stagestostable,thenplace1HumanFirstanydistrict.24/7maydecrease1unreststageorremove1orgcrime.',
['Circusstrike2downstable','then1HumanFirstanydistrict','24/7oneunrestdecreaseOR1orgcrimeremoval'],['Printed Media0–9; RR68'],'Fixed later placement and a genuine mutually exclusive action branch.')
add('Full Deployment chooses another player. Who chooses between its effects and chooses the card type, what are those effects, and may the resolver target themself?',
'Resolverchoosesanotherplayerandeitherdraw5ofresolverschosentypeorfliprecipientemergencyfaceup; notself,recipientdoesnotchooseoption/type.',
['resolverchoosesanothernotself','resolverchoosesdraw5typeorflipemergencyup','drawtypechosenresolver'],['Printed Security5–9'],'Chooser/recipient distinction and emergency restoration alternative.')
add('For Riot Control, what component is removed first, what may then be removed and from where, what unrest consequence follows, and is the sacrificed prisec an enemy for Globalsec’s contract?',
'Remove1prisecfromanydistrict toremoveupto2enemiesfromcity; then+1unrestin1districtnotstrike/outage. Prisecnotenemy,sosacrificealone nopayoutGlobalsec.',
['first1prisecfromdistrict','upto2enemiescity','then+1unrestonelegal district','prisecnotenemy'],['Printed Security10–14; RR23'],'Removal cost and permitted followup with nonenemy sacrifice; no impossible-cost ruling assumed.')
add('State Arrest Orders’ printed placement/removal instruction and distinguish units from tokens. State Scorched Earth’s required outage destination and the geographic scope of enemy removal. Do not assume an impossible-cost or simultaneous-priority ruling.',
'ArrestOrdersplaces1prisecinanydistrict toremoveallotherunits there; doesnotinstructremovingtokens. ScorchedEarthplaces1outageindistrictnotinoutage toremoveallenemiesthereandinanotherdistrictinsametier.',
['Arrest1prisecanydistrict toremoveallotherunits nottokens','Scorchedoutageindistrictnotoutage','allenemiesthereandoneotherdistrictsametier'],['Printed Security0–4,15–19'],'Specific removal versus generic prisec movement and same-tier range restrictions; deliberately no unsourced blocked-cost adjudication.')
add('Gentrification is resolved in a district with an outage and enemy units. What happens in order, what if prisec is already present, and do those forced enemy movements count as removals for Globalsec?',
'Removeoutage, thenplace1prisecifnonepresent; eachenemytheremoves. Existingprisecmeansdonotaddsecond. EnemyforcedmovementnotremovalnopaymentGlobalsec; outageremovalcanpayWeyland.',
['removeoutagebeforeprisec','place1ifnonealready','enemiesmove notremoved','noGlobalsecremovalpayout'],['Printed Construction5–9; RR35,42'],'Conditional prisec placement following outage removal, with explicit move rather than removal.')
add('Budget Renovations removes two outages. Which districts gain unrest, at what stage do they finish if nothing else intervenes, and can the unrest penalty be placed elsewhere?',
'Upto2outagesremoved; eachdistrictwhereactuallyremovedthen+1unrest,stableafteroutageremovalthentoprotest. Notelsewhere.',
['upto2outageremoval','eachactualremovaldistrict+1thenprotest','cannotredirectelsewhere'],['Printed Construction10–14; RR68.10'],'Linked followup destinations and removal-then-unrest state change.')
add('Vanity Project chooses a player who supported its offer but has no assets. What capital is awarded, is the grant prevented by having no asset to discard, and how would a nonsupporter’s grant differ?',
'Supporter4capital;nonsupporter2. Then1assetdiscardifpossible; noassetdoesnotpreventgrant.',
['supporter4nonsupporter2','discard1ifpossible','noassetdoesnotblockcapital'],['Printed Construction15–19'],'Support-dependent grant plus explicit if-possible followup branch.')
add('For Clean Slate, how many illnesses may be removed, where must its later outage be placed, and does illness add threat during it? How does Clinical Trials differ in removal amount and illness handling?',
'CleanSlateupto2illnessfromcity; then1outageinadistrictwhereillnessremoved; immunity. ClinicalTrialsremove1illnessanydistrictalsoimmune.',
['CleanSlateupto2','outagewhereactuallyremovedillness','bothillnessimmune','Clinical1anydistrict'],['Printed Biotech0–9'],'Linked later placement location and explicit immunity across two distinct removal forms; no unsupported impossible-cost rule.')
add('In a five-player Information Procurement, contributions in active-clockwise order total4 or total6. What is the threat change in each, is each player required to pay1, and is overpaying forbidden?',
'At4threshold5notmet,noreduction.6>=5reduces2threat. Eachcanpayanyamountnotrequired1; overpayallowed.',
['thresholdplayercount5','4noreduce6reduce2','eachanyamount activeclockwise','overpaylegal'],['Printed Biotech10–14'],'Collective threshold payment with voluntary unequal contributions and overpayment branch.')
add('For Unorthodox Knowledge, how many event cards are inspected, where are they returned and in what order, and may their fronts be shared?',
'Top3look;1tobottom,other2topanyorder. Frontssecret,backsopen.',
['looktop3','1bottomresttopanyorder','frontssecretbacksopen'],['Printed Biotech15–19; RR24.3'],'Actual event-reordering procedure not tested by seed Caprice exception.')
add('Energy Sector has supply3 against demand4, then consider supply0 against demand0 and supply5 against demand2. What capital is earned in each, and does its formula count all supply or only surplus?',
'First0becausemissdemand.0meeting0earns3.5meeting2formula3+2*5=13capped7. Countsallsupplynotsurplus.',
['3<4zero','0=0earns3','5>=2earns7capafter13formula','totalsupplynotexcess'],['Printed investment1; FAQ Investments'],'Positive sector formula/cap plus zero-demand base branch; seed tests eligibility only.')
add('Banking and Entertainment Sector each have supply5 meeting demand. Retail has consumables2 meeting demand; Technology has tech1 meeting demand. Calculate each capital award and state the corresponding formula/cap.',
'Bankingmin6(2+5)=6;Entertainmentlikewise6. Retailmin6(2+2*2)=6. Technologymin6(3+1)=4.',
['Bankingformula2+Smax6case6','Entertainmentformula2+Smax6case6','Retail2+2Smax6case6','Technology3+Smax6case4'],['Printed investments0,2,8,10'],'Remaining distinct printed sector formulas in one reference question; no added questions for identical Banking/Entertainment formula.')
add('At investment scoring there are3 illness tokens,1 orgcrime,2 prisec,2 outages and4 Human First in the city. What are Healthcare Initiative, Laundering Scheme, Militarized Police, Power Siphoning and Union Agreement’s awards? Are tier awards cumulative?',
'Healthcare5,Laundering0,Militarized6,Power5,Union7. Tierawardsnotcumulative;belowfirstthresholdnoaward.',
['Healthcare3illness5','Laundering1org0','Militarized2prisec6','Power2outage5','Union4HF7','tiersnotcumulativebelowthreshold0'],['Printed investments3–5,7,11'],'Count-threshold investment family with below-threshold and noncumulative outcomes; no cosmetic count variants added.')
add('For Populist Dismissal, two districts are in protest, three in strike and two in outage. What is its award? For Short Sale, supply amounts across five resource types are0,1,1,2,4: what is the award and what is being counted?',
'Populist5capital(protest+strike,notoutage stable). ShortSale3resourcetypesat1orless =>7capital,notnumberofindividualresources.',
['Populist2+3=5outagesexcluded','ShortSale0,1,1threequalifyingtypes','ShortSale7','typesnotresourceunits'],['Printed investments6,9; RR39,68'],'Unrest category exclusion and low-resource-type counting investment branches.')
add('Helium-3 Transport Threatened is revealed with outages in both tier2 and tier3; then consider outages only in tier1. What upper-half threat result applies in each, and is the check before or after its lower placement list?',
'Both2and3means+5only,tier3prioritynot5+3. Onlytier1meansneithercondition,noupperthreat. Checkupperbeforelowerplacements.',
['bothhigher+5not8','onlytier1noincrease','uppercheckbeforeplacements'],['Printed event2; RR24–25'],'Hierarchical event else-if and no-qualifying-tier branch.')
add('Human First Starts Riot has a Human First in tier2; Beanstalk Beset by Protesters has one in tier3. What does each upper effect do? If its required tier has no Human First, what happens instead and in what order?',
'Riottier2+2;Besettier3+4. OtherwiseeachHFmovesonce highestdistrictfirst. Conditionalbranchesdonotbothhappen.',
['Riot+2tier2','Beset+4tier3','otherwiseallHFoncehighestfirst','conditionexcludesmovementbranch'],['Printed events1,13'],'Conditional fixed-threat versus movement event family; two tier variants consolidated.')
add('For Beanstalk Owned by Mob? and Pistoleros Hit Squads Strike!, which tier triggers the upper fixed threat and how much? If the relevant tier is empty but orgcrime exists elsewhere, what happens instead? Can those moves still increase threat?',
'Ownedtier3+4;Pistoleros tier2+3. Elseallorgmovehighestfirst;Rootentriesstill+2each,evenifupperfixedthreatnotapplied.',
['Ownedtier3+4','Pistoleros tier2+3','elseallorghighestfirst','Root+2eachpossible'],['Printed events10,15; RR35,63'],'Orgcrime conditional movement branch and consequent Root threat; not merely changed numbers from Human First because class/Root resolution independently mapped.')
add('Activist Cells Awaken is resolved with Human First in several districts. What is the movement order and how many moves per unit, and do duplicate/prisec blocking and the Root still apply?',
'Highestnumberedfirst,eachHumanFirstmovestwice; normalcascadingblocksandRootreserve+2apply.',
['highestfirst','each2moves','normalblockcascadeandRoot+2reserve'],['Printed event9; RR35–36'],'Explicit twice-moving event exception beyond one-move conditional events.')
add('Explain the different upper-half conditions for Report: Record Unemployment, Average Wage Falls Again and Earthquake Rocks City, including what happens below their thresholds. What do Social Apps Spark Revolution and Welfare Programs Slashed count?',
'Report6+protestorstrike=>4;below0. Average3+strike=>4;below0. Earthquake3+outage=>5;below0. Social+1eachprotestorstrike;Welfare+1eachstrikeonly.',
['Report6protestorstrike+4else0','Average3strike+4else0','Earthquake3outage+5else0','Socialcountsprotest+strike','Welfarestrikeonly'],['Printed events0,3,6,11,14'],'Threshold versus per-district event branches, including protest-versus-strike distinction.')
add('What do Humanity Labor Hosts Union Heads, Gang Wars at All-Time High!/Tri-Maf Leaders Unite!, and Crumbling Infrastructure/Rolling Outages Increase count for upper-half threat? Are new lower-half placements included in that earlier count?',
'1percurrentHumanFirst,orgcrime,andoutagedistrictrespectively. Countbeforelowerplacements;newplacementsnotretroactivelyincludedbutRootspilloverscanaddseparatethreat.',
['1perHF','1perorgcrime','1peroutagedistrict','beforeplacementsnotretroactive','placementRootseparatethreat'],['Printed events4–5,7–8,12; RR24'],'Per-component event counting grouped by identical formulas; distinct earlier-count versus later-placement timing.')
add('How many standard and demand rounds are in the core game, when are demand rounds interleaved, and does a demand round contain the ordinary Action/Production/Event sequence?',
'There are six standard rounds and three demands, one demand after each pair of standards. Demands use Score Investment, Pay Demand, Reveal Demand, Choose Investment instead of ordinary phases, with final-demand last steps omitted.',
['six standard three demand','demand after each pair standards','demand has own steps rather than normal phases'],['RR18,51,55; LTP pp8–9 round-track diagram'],'Complete source pass found round counts/interleaving not actually asked by original phase/demand questions.')
add('A player has seven action cards when someone else ends their turn. Must that player immediately discard to five? When is the normal hand-size check made and which player discards?',
'No. At the end of the active player’s own turn after End of Turn abilities, that active player discards to their own hand limit; others are not checked merely because a turn ends.',
['no discard at another turn end','active own end after abilities checks own limit'],['RR3.3,30.2'],'Actor-specific hand check exposes a distinct outcome branch beyond the active-turn procedure.')
add('Several ordinary counteroffers remain faceup in the Counteroffer box. Which one can win and resolve, can an earlier one resolve instead, and what role do the earlier cards retain?',
'Only the topmost current counteroffer is operative; earlier ones cannot win or resolve merely from remaining faceup. Earlier faceup cards count toward the extra discard cost of a later counteroffer.',
['topmost only operative','earlier not resolve','earlier retained for proposal-cost count'],['RR15.3–15.5'],'Scope pass confirmed topmost-only rule was key background, not actually asked in seed Q05.')
add('How do you identify primary and secondary resource icons? If a district has only one resource icon and an orgcrime unit plus a development, what can it produce under ordinary production?',
'Primary is leftmost circled icon; secondary is other uncircled icon. Single icon is primary with no secondary; orgcrime blocks that only resource even with development, so produces none.',
['primary leftmost circled secondary uncircled','one icon primary no secondary','orgcrime blocks even developed so none'],['RR19.2–19.3,38.4–38.5,41,52'],'Explicit single-resource classification and no-secondary outcome not actually asked by the two-resource example.')
add('Threat is23 when an event’s upper effect adds2, before its lower-half placements. The Federalist has24 capital. Must players finish those placements or wait for later income before determining the result, and who wins?',
'Threat25 ends immediately; stop remaining placements and do not wait for later income. Federalist24 is below25, so Federalist and all ordinary players lose.',
['immediate stop at25 before later placements/income','Federalist24 loses','ordinary all lose'],['RR24–25,28,63.1,69.3'],'An in-progress event ending branch differs from completing the final demand after investment scoring.')
add('Describe ordinary unrest stages and token representation. What are the results of decreasing strike by1, protest by1, and stable by1, and what unrest remains after removing an outage?',
'Stable has no unrest token, protest protest side, strike strike side. Strike minus1 becomes protest; protest minus1 becomes stable and returns token to reserve; stable cannot decrease. Outage removal leaves stable.',
['three stages token none/protest/strike sides','strike decrease1protest','protest decrease1stable remove token','stable cannot decrease','outage removal stable'],['RR39,45,54,57,68'],'Reverse unrest transitions and representations were not directly asked in prior Human First/increase questions.')
add('If Learn to Play and Rules Reference conflict, which controls? If an asset contradicts Rules Reference, what controls, and should both be followed when compatible? How are the official2018 FAQ corrections treated?',
'Rules Reference overrides Learn to Play. Contradicting asset text takes priority over RR; obey both if compatible. Official2018FAQ errata/corrections apply to corrected printed text.',
['RR over LTP','asset over RR on contradiction','follow both compatible','official2018FAQ corrections apply'],['RR p2 Golden Rules; FAQ Errata'],'Explicit authority/compatibility rule governs card-specific exceptions and was not directly asked elsewhere.')
# This file creates a candidate expansion only. Seed pass and independent scope/coverage review precede final full-bank freeze.
out=B/'expanded-candidate-v1';out.mkdir(exist_ok=True)
q={'game':'New Angeles','scope':baseq['scope'],'benchmark_version':'expanded-candidate-v1','questions':questions};k={**basek,'benchmark_version':'expanded-candidate-v1','answers':answers}
for name,obj in [('questions.json',q),('answer-key.json',k),('accepted-candidates.json',novel)]: (out/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
print('Candidate bank',len(questions),'questions; original20unchanged from corrected seed-v2.')

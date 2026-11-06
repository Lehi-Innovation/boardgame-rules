var Types;
(function (Types) {
    function getCardProperties() {
        const dummyEventDesc = new EventDesc("", "");
        const dummyPower = new PowerCard();
        const dummyFear = new FearCard();
        const dummyChoiceEvent = new ChoiceEventCard();
        const dummyStageEvent = new StageEventCard(null, dummyEventDesc, dummyEventDesc, dummyEventDesc);
        const dummyTerrorLevelEvent = new TerrorLevelEventCard(null, dummyEventDesc, dummyEventDesc, dummyEventDesc);
        const dummyHealthyBlightedLandEvent = new HealthyBlightedLandEventCard(null, dummyEventDesc, dummyEventDesc);
        const dummyAdversaryEvent = new AdversaryEvent(null, null, null, dummyStageEvent);
        let props = Object.getOwnPropertyNames(dummyPower)
            .concat(Object.getOwnPropertyNames(dummyFear))
            .concat(Object.getOwnPropertyNames(dummyChoiceEvent))
            .concat(Object.getOwnPropertyNames(dummyStageEvent))
            .concat(Object.getOwnPropertyNames(dummyTerrorLevelEvent))
            .concat(Object.getOwnPropertyNames(dummyHealthyBlightedLandEvent))
            .concat(Object.getOwnPropertyNames(dummyAdversaryEvent))
            .filter((name) => name.toLowerCase() == name);
        props = [...new Set(props)];
        return props;
    }
    Types.getCardProperties = getCardProperties;
    let Speed;
    (function (Speed) {
        Speed["Fast"] = "Fast";
        Speed["Slow"] = "Slow";
    })(Speed = Types.Speed || (Types.Speed = {}));
    let Land;
    (function (Land) {
        Land["Ocean"] = "Ocean";
        Land["Jungle"] = "Jungle";
        Land["Wetland"] = "Wetland";
        Land["Mountain"] = "Mountain";
        Land["Sands"] = "Sands";
        Land["Coastal"] = "Coastal";
        Land["Inland"] = "Inland";
    })(Land = Types.Land || (Types.Land = {}));
    Types.LandAny = [Land.Ocean, Land.Jungle, Land.Wetland, Land.Mountain, Land.Sands, Land.Coastal];
    let TargetSpirit;
    (function (TargetSpirit) {
        TargetSpirit["Any"] = "Any Spirit";
        TargetSpirit["Another"] = "Another Spirit";
        TargetSpirit["Yourself"] = "Yourself";
    })(TargetSpirit = Types.TargetSpirit || (Types.TargetSpirit = {}));
    let TargetProperty;
    (function (TargetProperty) {
        TargetProperty["Dahan"] = "Dahan";
        TargetProperty["TwoDahan"] = "2 Dahan";
        TargetProperty["Invaders"] = "Invaders";
        TargetProperty["Town"] = "Town";
        TargetProperty["City"] = "City";
        TargetProperty["Blight"] = "Blight";
        TargetProperty["NoBlight"] = "No Blight";
        TargetProperty["NoInvaders"] = "No Invaders";
        TargetProperty["NoWetland"] = "No Wetland";
        TargetProperty["Beasts"] = "Beasts";
        TargetProperty["TwoBeasts"] = "2 Beasts";
        TargetProperty["Inland"] = "Inland";
        TargetProperty["Disease"] = "Disease";
        TargetProperty["Strife"] = "Strfe";
        TargetProperty["Incarna"] = "Incarna";
    })(TargetProperty = Types.TargetProperty || (Types.TargetProperty = {}));
    let Source;
    (function (Source) {
        Source["Presence"] = "Presence";
        Source["SacredSite"] = "SacredSite";
    })(Source = Types.Source || (Types.Source = {}));
    class Ranges {
        constructor(from, range, land, landProperty) {
            this.from = from;
            this.range = range;
            this.land = land;
            this.landProperty = landProperty;
        }
        toString() {
            let res = this.from + "";
            if (this.land) {
                res += " on " + this.land;
            }
            if (this.landProperty) {
                res += " with " + this.landProperty;
            }
            res += ": ";
            if (Array.isArray(this.range)) {
                res += this.range.join(" & ");
            }
            else {
                res += this.range;
            }
            return res;
        }
        valueOf() {
            if (Array.isArray(this.range)) {
                return Math.max.apply(null, this.range);
            }
            return this.range;
        }
    }
    Types.Ranges = Ranges;
    let Elements;
    (function (Elements) {
        Elements["Sun"] = "Sun";
        Elements["Moon"] = "Moon";
        Elements["Fire"] = "Fire";
        Elements["Air"] = "Air";
        Elements["Water"] = "Water";
        Elements["Earth"] = "Earth";
        Elements["Plant"] = "Plant";
        Elements["Animal"] = "Animal";
    })(Elements = Types.Elements || (Types.Elements = {}));
    let ProductSet;
    (function (ProductSet) {
        ProductSet["Basegame"] = "Basegame";
        ProductSet["BranchAndClaw"] = "Branch & Claw";
        ProductSet["JaggedEarth"] = "Jagged Earth";
        ProductSet["Promo"] = "Promo";
        ProductSet["Promo2"] = "Promo2";
        ProductSet["HorizonsOfSpiritIsland"] = "Horizons of Spirit Island";
        ProductSet["NatureIncarnate"] = "Nature Incarnate";
    })(ProductSet = Types.ProductSet || (Types.ProductSet = {}));
    let Unique;
    (function (Unique) {
        Unique["ASpreadOfRampantGreen"] = "Unique Power: A Spread of Rampant Green";
        Unique["BringerOfDreamsAndNightmares"] = "Unique Power: Bringer of Dreams and Nightmares";
        Unique["LightningsSwiftStrike"] = "Unique Power: Lightning's Swift Strike";
        Unique["OceansHungryGrasp"] = "Unique Power: Ocean's Hungry Grasp";
        Unique["RiverSurgesInSunlight"] = "Unique Power: River Surges in Sunlight";
        Unique["ShadowsFlickerLikeFlame"] = "Unique Power: Shadows Flicker Like Flame";
        Unique["Thunderspeaker"] = "Unique Power: Thunderspeaker";
        Unique["VitalStrengthOfTheEarth"] = "Unique Power: Vital Strength of the Earth";
        Unique["SharpFangsBehindTheLeaves"] = "Unique Power: Sharp Fangs behind the Leaves";
        Unique["KeeperOfTheForbiddenWilds"] = "Unique Power: Keeper of the Forbidden Wilds";
        Unique["SerpentSlumberingBeneathTheIsland"] = "Unique Power: Serpent Slumbering Beneath the Island";
        Unique["HeartOfTheWildfire"] = "Unique Power: Heart of the Wildfire";
        Unique["FinderOfPathsUnseen"] = "Unique Power: Finder of Paths Unseen";
        Unique["FracturedDaysSplitTheSky"] = "Unique Power: Fractured Days Split the Sky";
        Unique["GrinningTricksterStirsUpTrouble"] = "Unique Power: Grinning Trickster Stirs Up Trouble";
        Unique["LureOfTheDeepWilderness"] = "Unique Power: Lure of the Deep Wilderness";
        Unique["ManyMindsMoveAsOne"] = "Unique Power: Many Minds Move as One";
        Unique["ShiftingMemoryOfAges"] = "Unique Power: Shifting Memory of Ages";
        Unique["ShroudOfSilentMist"] = "Unique Power: Shroud of Silent Mist";
        Unique["StarlightSeeksItsForm"] = "Unique Power: Starlight Seeks its Form";
        Unique["StonesUnyieldingDefiance"] = "Unique Power: Stone's Unyielding Defiance";
        Unique["VengeanceAsABurningPlague"] = "Unique Power: Vengeance as a Burning Plague";
        Unique["VolcanoLoomingHigh"] = "Unique Power: Volcano Looming High";
        Unique["DownpourDrenchesTheWorld"] = "Unique Power: Downpour Drenches the World";
        // Horizons
        Unique["DevouringTeethLurkUnderfoot"] = "Unique Power: Devouring Teeth Lurk Underfoot";
        Unique["EyesWatchFromTheTrees"] = "Unique Power: Eyes Watch From the Trees";
        Unique["FathomlessMudOfTheSwamp"] = "Unique Power: Fathomless Mud of the Swamp";
        Unique["RisingHEatOfStoneAndSand"] = "Unique Power: Rising Heat of Stone and Sand";
        Unique["SunBrightWhirlwind"] = "Unique Power: Sun-Bright Whirlwind";
        // Nature Incarnate
        Unique["BreathOfDarknessDownYourSpine"] = "Unique Power: Breath of Darkness Down Your Spine";
        Unique["DancesUpEarthquakes"] = "Unique Power: Dances Up Earthquakes";
        Unique["EmberEyedBehemoth"] = "Unique Power: Ember-Eyed Behemoth";
        Unique["HearthVigil"] = "Unique Power: Hearth-Vigil";
        Unique["RelentlessGazeOfTheSun"] = "Unique Power: Relentless Gaze of the Sun";
        Unique["ToweringRootsOfTheJungle"] = "Unique Power: Towering Roots of the Jungle";
        Unique["WanderingVoiceKeensDelirium"] = "Unique Power: Wandering Voice Keens Delirium";
        Unique["WoundedWatersBleeding"] = "Unique Power: Wounded Waters Bleeding";
    })(Unique = Types.Unique || (Types.Unique = {}));
    let PowerDeckType;
    (function (PowerDeckType) {
        PowerDeckType["Minor"] = "Minor Power";
        PowerDeckType["Major"] = "Major Power";
    })(PowerDeckType = Types.PowerDeckType || (Types.PowerDeckType = {}));
    let FearType;
    (function (FearType) {
        FearType["Fear"] = "Fear";
    })(FearType = Types.FearType || (Types.FearType = {}));
    let EventType;
    (function (EventType) {
        EventType["ChoiceEvent"] = "Choice Event";
        EventType["StageEvent"] = "Stage Event";
        EventType["TerrorLevelEvent"] = "Terror Level Event";
        EventType["HealthyBlightedLandEvent"] = "Healthy Blighted Island Event";
        EventType["AdversaryEvent"] = "Adversary Event";
    })(EventType = Types.EventType || (Types.EventType = {}));
    let BlightType;
    (function (BlightType) {
        BlightType["BlightedIsland"] = "Blighted Island";
        BlightType["StillHealthyIsland"] = "Still-Healthy Island (for now)";
    })(BlightType = Types.BlightType || (Types.BlightType = {}));
    let Adversary;
    (function (Adversary) {
        Adversary["KingdomOfFrance"] = "Kingdom of France";
    })(Adversary = Types.Adversary || (Types.Adversary = {}));
    let Stage;
    (function (Stage) {
        Stage[Stage["Stage1"] = 0] = "Stage1";
        Stage[Stage["Stage2"] = 1] = "Stage2";
        Stage[Stage["Stage3"] = 2] = "Stage3";
    })(Stage = Types.Stage || (Types.Stage = {}));
    let TerrorLevel;
    (function (TerrorLevel) {
        TerrorLevel[TerrorLevel["TerrorLevel1"] = 0] = "TerrorLevel1";
        TerrorLevel[TerrorLevel["TerrorLevel2"] = 1] = "TerrorLevel2";
        TerrorLevel[TerrorLevel["TerrorLevel3"] = 2] = "TerrorLevel3";
    })(TerrorLevel = Types.TerrorLevel || (Types.TerrorLevel = {}));
    let HealthyBlightedLand;
    (function (HealthyBlightedLand) {
        HealthyBlightedLand[HealthyBlightedLand["Healthy"] = 0] = "Healthy";
        HealthyBlightedLand[HealthyBlightedLand["Blighted"] = 1] = "Blighted";
    })(HealthyBlightedLand = Types.HealthyBlightedLand || (Types.HealthyBlightedLand = {}));
    function powerToColor(type) {
        switch (type) {
            case PowerDeckType.Minor:
                return "rgba(50, 50, 50, 0.3)";
            case PowerDeckType.Major:
                return "rgba(255, 255, 0, 0.25)";
            case Unique.ASpreadOfRampantGreen:
            case Unique.BringerOfDreamsAndNightmares:
            case Unique.LightningsSwiftStrike:
            case Unique.OceansHungryGrasp:
            case Unique.RiverSurgesInSunlight:
            case Unique.ShadowsFlickerLikeFlame:
            case Unique.Thunderspeaker:
            case Unique.VitalStrengthOfTheEarth:
            case Unique.SharpFangsBehindTheLeaves:
            case Unique.KeeperOfTheForbiddenWilds:
            case Unique.HeartOfTheWildfire:
            case Unique.SerpentSlumberingBeneathTheIsland:
            case Unique.FinderOfPathsUnseen:
            case Unique.FracturedDaysSplitTheSky:
            case Unique.GrinningTricksterStirsUpTrouble:
            case Unique.LureOfTheDeepWilderness:
            case Unique.ManyMindsMoveAsOne:
            case Unique.ShiftingMemoryOfAges:
            case Unique.ShroudOfSilentMist:
            case Unique.StarlightSeeksItsForm:
            case Unique.StonesUnyieldingDefiance:
            case Unique.VengeanceAsABurningPlague:
            case Unique.VolcanoLoomingHigh:
            case Unique.DownpourDrenchesTheWorld:
            case Unique.DevouringTeethLurkUnderfoot:
            case Unique.EyesWatchFromTheTrees:
            case Unique.FathomlessMudOfTheSwamp:
            case Unique.RisingHEatOfStoneAndSand:
            case Unique.SunBrightWhirlwind:
            case Unique.BreathOfDarknessDownYourSpine:
            case Unique.DancesUpEarthquakes:
            case Unique.EmberEyedBehemoth:
            case Unique.HearthVigil:
            case Unique.RelentlessGazeOfTheSun:
            case Unique.ToweringRootsOfTheJungle:
            case Unique.WanderingVoiceKeensDelirium:
            case Unique.WoundedWatersBleeding:
                return "rgba(0, 128, 0, 0.25)";
            default:
                throw new Error();
        }
    }
    class Card {
        constructor(set, type, name) {
            this.set = set;
            this.type = type;
            this.name = name;
            // capital so they can not be searched with filters
            this.FontSize = null;
            this.P = null;
            this.Container = null;
            this.Flex = null;
        }
        getSearchString() {
            return Object.keys(this)
                .filter((name) => name.toLowerCase() === name)
                .map((name) => this[name])
                .filter((prop) => prop !== null)
                .map((prop) => prop.toString().toLowerCase().replace("&", "and"))
                .join(" ")
                .toLowerCase();
        }
        getCardFlexElement() {
            if (this.Flex != null) {
                return this.Flex;
            }
            let flex = document.createElement("div");
            this.Flex = flex;
            flex.classList.add("flex-50", "xs-flex-33", "sm-flex-25", "md-flex-20", "l-flex-15", "xl-flex-12", "xxl-flex-10");
            let container = document.createElement("div");
            this.Container = container;
            container.classList.add("flip-container");
            let flipper = document.createElement("div");
            flipper.classList.add("flipper");
            let front = document.createElement("div");
            front.classList.add("front");
            front.style.cursor = "pointer";
            // image with webp by default and jpg as fallback
            let picture = document.createElement("picture");
            let webp = document.createElement("source");
            webp.srcset = this.getImagePath() + ".webp";
            webp.type = "image/webp";
            picture.appendChild(webp);
            let jpg = document.createElement("source");
            jpg.srcset = this.getImagePath() + ".jpg";
            jpg.type = "image/jpg";
            picture.appendChild(jpg);
            let fallback = document.createElement("img");
            fallback.src = this.getImagePath() + ".jpg";
            picture.appendChild(fallback);
            front.appendChild(picture);
            if (this.getFrontOverlay() != null) {
                front.appendChild(this.getFrontOverlay());
            }
            let back = document.createElement("div");
            back.classList.add("back");
            back.style.cursor = "pointer";
            let backdiv = document.createElement("div");
            backdiv.style.paddingLeft = "10px";
            backdiv.style.paddingRight = "10px";
            let p = document.createElement("span");
            this.P = p;
            p.style.cursor = "auto";
            p.innerHTML = this.getBacksideText();
            backdiv.appendChild(p);
            back.appendChild(backdiv);
            flipper.appendChild(back);
            flipper.appendChild(front);
            container.appendChild(flipper);
            flex.appendChild(container);
            let x, y;
            container.onmousedown = (e) => {
                x = e.x;
                y = e.y;
            };
            container.onmouseup = (e) => {
                if (e.target instanceof HTMLAnchorElement) {
                    // link was clicked - ignore
                    return;
                }
                if (Math.abs(x - e.x) > 5 || Math.abs(y - e.y) > 5) {
                    // it was a drag (e.g. to select and copy something) - ignore
                    return;
                }
                if (!container.classList.contains("flipped")) {
                    if (this.FontSize == null) {
                        this.scaleFontSize();
                    }
                    else {
                        p.style.fontSize = this.FontSize + "px";
                    }
                }
                container.classList.toggle("flipped");
            };
            return flex;
        }
        getImagePath() {
            let name;
            if (Array.isArray(this.name)) {
                name = this.name[0];
            }
            else {
                name = this.name;
            }
            return this.getImageFolder() + name
                .toLowerCase()
                .replace(/ /g, "_")
                .replace(/[^a-z_]/g, "");
        }
        // scale font of cardbacks to fit size
        scaleFontSize() {
            let p = this.P;
            this.FontSize = 16;
            p.style.fontSize = this.FontSize + "px";
            let back = p.parentElement.parentElement;
            while (p.offsetHeight > back.offsetHeight) {
                this.FontSize -= 0.5;
                p.style.fontSize = this.FontSize + "px";
            }
        }
        onresize() {
            this.FontSize = null;
            if (this.P != null && this.Container != null && this.Container.classList.contains("flipped")) {
                this.scaleFontSize();
            }
        }
    }
    Types.Card = Card;
    class PowerCard extends Card {
        constructor(set, type, name, cost, speed, range, target, elements, artist, description) {
            super(set, type, name);
            this.cost = cost;
            this.speed = speed;
            this.range = range;
            this.target = target;
            this.elements = elements;
            this.artist = artist;
            this.description = description;
        }
        getSearchString() {
            let s = this.set.replace(/&/g, "and") + " " + this.type + " " + this.cost + " " + this.name + " " + this.speed;
            if (this.range != null) {
                s += " " + this.range.toString().replace(/&/g, "and");
            }
            if (this.target == Types.LandAny) {
                s += " Any";
            }
            else {
                s += " " + this.target;
            }
            s += " " + this.elements + " " + this.description + " " + this.artist;
            return s.toLowerCase();
        }
        getFrontOverlay() {
            let overlay = document.createElement("div");
            overlay.style.position = "absolute";
            overlay.style.backgroundColor = powerToColor(this.type);
            overlay.style.width = "67%";
            overlay.style.height = "10%";
            overlay.style.left = "27%";
            overlay.style.top = "4%";
            overlay.style.zIndex = "1";
            overlay.style.borderRadius = "0 13px 0 0";
            return overlay;
        }
        getBacksideText() {
            let text = "";
            text += "<b>Set</b>: " + this.set + "<br/>";
            text += "<b>Type</b>: " + this.type + "<br/>";
            text += "<b>Name</b>: " + this.name + "<br/>";
            text += "<b>Cost</b>: " + this.cost + "<br/>";
            text += "<b>Speed</b>: " + this.speed + "<br/>";
            if (this.range != null) {
                text += "<b>Range</b>: " + this.range.toString() + "<br/>";
            }
            let target = "";
            if (Array.isArray(this.target)) {
                if (this.target == Types.LandAny) {
                    target = "Any";
                }
                else {
                    target = this.target.join(", ");
                }
            }
            else if (this.target == null) {
                target = "";
            }
            else {
                target = this.target;
            }
            text += "<b>Target</b>: " + target + "<br/>";
            text += "<b>Elements</b>: " + this.elements.join(", ") + "<br/>";
            text += "<b>Description</b>: " + this.description + "<br/>";
            text += "<b>Artist</b>: " + this.artist + "<br/>";
            let type = this.type;
            const tag = type.startsWith("Unique") ? this.name + " (" + type.substring(14) + ")" : this.name;
            text += "<a href=\"https://querki.net/u/darker/spirit-island-faq/#!"
                + encodeURIComponent(tag) + "\" target='_blank'>FAQ</a><br/>";
            return text;
        }
        getImageFolder() {
            return "imgs/powers/";
        }
    }
    Types.PowerCard = PowerCard;
    class FearCard extends Card {
        constructor(set, type, name, level1, level2, level3) {
            super(set, type, name);
            this.name = name;
            this.level1 = level1;
            this.level2 = level2;
            this.level3 = level3;
            // set description for searching
            this.description = level1 + " " + level2 + " " + level3;
        }
        getImageFolder() {
            return "imgs/fears/";
        }
        getBacksideText() {
            let text = "";
            text += "<b>Set</b>: " + this.set + "<br/>";
            text += "<b>Type</b>: " + this.type + "<br/>";
            text += "<b>Name</b>: " + this.name + "<br/>";
            text += "<b>Level 1</b>: " + this.level1 + "<br/>";
            text += "<b>Level 2</b>: " + this.level2 + "<br/>";
            text += "<b>Level 3</b>: " + this.level3 + "<br/>";
            text += "<a href=\"https://querki.net/u/darker/spirit-island-faq/#!"
                + encodeURIComponent(this.name) + "\" target='_blank'>FAQ</a><br/>";
            return text;
        }
        getFrontOverlay() {
            return null;
        }
    }
    Types.FearCard = FearCard;
    class EventCard extends Card {
        constructor(set, type, name, tokenevent, dahanevent) {
            super(set, type, name);
            this.tokenevent = tokenevent;
            this.dahanevent = dahanevent;
        }
        getImageFolder() {
            return "imgs/events/";
        }
        getFrontOverlay() {
            return null;
        }
    }
    Types.EventCard = EventCard;
    class ChoiceCost {
        constructor(energy, per, aidedBy) {
            this.energy = energy;
            this.per = per;
            this.aidedBy = aidedBy;
        }
        toString() {
            let text = "";
            text += this.energy + " Energy";
            if (this.per !== null) {
                text += " per " + this.per + ".";
            }
            else {
                text += ".";
            }
            if (this.aidedBy !== null) {
                text += " Aided by " + this.aidedBy + ".";
            }
            return text;
        }
    }
    Types.ChoiceCost = ChoiceCost;
    class ChoiceDesc {
        constructor(name, cost, actions) {
            this.name = name;
            this.cost = cost;
            this.actions = actions;
        }
        toString() {
            let text = "";
            text += this.name;
            if (this.cost != null) {
                text += "<br/>Cost: " + this.cost;
            }
            for (let action of this.actions) {
                text += "<br/>• " + action;
            }
            return text;
        }
    }
    Types.ChoiceDesc = ChoiceDesc;
    class ChoiceEventCard extends EventCard {
        constructor(set, name, description, defaultactions, choices, tokenevent, dahanevent) {
            super(set, EventType.ChoiceEvent, name, tokenevent, dahanevent);
            this.description = description;
            this.defaultactions = defaultactions;
            this.choices = choices;
        }
        getBacksideText() {
            var _a;
            let text = "";
            text += "<b>Set</b>: " + this.set + "<br/>";
            text += "<b>Type</b>: " + this.type + "<br/>";
            text += "<b>Name</b>: " + this.name + "<br/>";
            text += "<b>Description</b>: " + this.description + "<br/>";
            for (let action of (_a = this.defaultactions) !== null && _a !== void 0 ? _a : []) {
                text += "• " + action + "<br/>";
            }
            for (let [i, choice] of this.choices.entries()) {
                text += "<b>Choice" + i + "</b>: " + choice + "<br/>";
            }
            if (this.tokenevent !== null) {
                text += "<b>Token Event</b>: " + this.tokenevent + "<br/>";
            }
            if (this.dahanevent !== null) {
                text += "<b>Dahan Event</b>: " + this.dahanevent + "<br/>";
            }
            text += "<a href=\"https://querki.net/u/darker/spirit-island-faq/#!"
                + encodeURIComponent(this.name) + "\" target='_blank'>FAQ</a><br/>";
            return text;
        }
    }
    Types.ChoiceEventCard = ChoiceEventCard;
    class EventDesc {
        constructor(name, description) {
            this.name = name;
            this.description = description;
        }
        toString() {
            return this.name + ": " + this.description;
        }
    }
    Types.EventDesc = EventDesc;
    class StageEventCard extends EventCard {
        constructor(set, level1, level2, level3, tokenevent, dahanevent) {
            super(set, EventType.StageEvent, [...new Set([level1.name, level2.name, level3.name])], tokenevent, dahanevent);
            this.level1 = level1;
            this.level2 = level2;
            this.level3 = level3;
        }
        getBacksideText() {
            let text = "";
            text += "<b>Set</b>: " + this.set + "<br/>";
            text += "<b>Type</b>: " + this.type + "<br/>";
            text += "<b>Name</b>: " + this.name + "<br/>";
            text += "<b>Level1</b>: " + this.level1 + "<br/>";
            text += "<b>Level2</b>: " + this.level2 + "<br/>";
            text += "<b>Level3</b>: " + this.level3 + "<br/>";
            if (this.tokenevent !== null) {
                text += "<b>Token Event</b>: " + this.tokenevent + "<br/>";
            }
            if (this.dahanevent !== null) {
                text += "<b>Dahan Event</b>: " + this.dahanevent + "<br/>";
            }
            for (const name of [...new Set([this.level1.name, this.level2.name, this.level3.name])]) {
                text += "<a href=\"https://querki.net/u/darker/spirit-island-faq/#!"
                    + encodeURIComponent(name) + "\" target='_blank'>FAQ: " + name + "</a><br/>";
            }
            return text;
        }
    }
    Types.StageEventCard = StageEventCard;
    class TerrorLevelEventCard extends EventCard {
        constructor(set, level1, level2, level3, tokenevent, dahanevent) {
            super(set, EventType.TerrorLevelEvent, [...new Set([level1.name, level2.name, level3.name])], tokenevent, dahanevent);
            this.level1 = level1;
            this.level2 = level2;
            this.level3 = level3;
        }
        getBacksideText() {
            let text = "";
            text += "<b>Set</b>: " + this.set + "<br/>";
            text += "<b>Type</b>: " + this.type + "<br/>";
            text += "<b>Name</b>: " + this.name + "<br/>";
            text += "<b>Level1</b>: " + this.level1 + "<br/>";
            text += "<b>Level2</b>: " + this.level2 + "<br/>";
            text += "<b>Level3</b>: " + this.level3 + "<br/>";
            if (this.tokenevent !== null) {
                text += "<b>Token Event</b>: " + this.tokenevent + "<br/>";
            }
            if (this.dahanevent !== null) {
                text += "<b>Dahan Event</b>: " + this.dahanevent + "<br/>";
            }
            for (const name of [...new Set([this.level1.name, this.level2.name, this.level3.name])]) {
                text += "<a href=\"https://querki.net/u/darker/spirit-island-faq/#!"
                    + encodeURIComponent(name) + "\" target='_blank'>FAQ: " + name + "</a><br/>";
            }
            return text;
        }
    }
    Types.TerrorLevelEventCard = TerrorLevelEventCard;
    class HealthyBlightedLandEventCard extends EventCard {
        constructor(set, healthy, blighted, tokenevent, dahanevent) {
            super(set, EventType.HealthyBlightedLandEvent, [healthy.name, blighted.name], tokenevent, dahanevent);
            this.healthy = healthy;
            this.blighted = blighted;
        }
        getBacksideText() {
            let text = "";
            text += "<b>Set</b>: " + this.set + "<br/>";
            text += "<b>Type</b>: " + this.type + "<br/>";
            text += "<b>Name</b>: " + this.name + "<br/>";
            text += "<b>Healthy</b>: " + this.healthy + "<br/>";
            text += "<b>Blighted</b>: " + this.blighted + "<br/>";
            if (this.tokenevent !== null) {
                text += "<b>Token Event</b>: " + this.tokenevent + "<br/>";
            }
            if (this.dahanevent !== null) {
                text += "<b>Dahan Event</b>: " + this.dahanevent + "<br/>";
            }
            for (const name of [this.healthy.name, this.blighted.name]) {
                text += "<a href=\"https://querki.net/u/darker/spirit-island-faq/#!"
                    + encodeURIComponent(name) + "\" target='_blank'>FAQ: " + name + "</a><br/>";
            }
            return text;
        }
    }
    Types.HealthyBlightedLandEventCard = HealthyBlightedLandEventCard;
    class AdversaryEvent extends EventCard {
        constructor(set, name, adversary, event) {
            let names = Array.isArray(event.name) ? [name].concat(event.name) : [name, event.name];
            super(set, [EventType.AdversaryEvent, event.type], names, event.tokenevent, event.dahanevent);
            this.Inner = event;
            this.adversary = adversary;
            let self = this;
            let old = Object.getOwnPropertyNames(new EventCard());
            let neu = Object.getOwnPropertyNames(event)
                .filter(prop => old.indexOf(prop) == -1);
            for (const prop of neu) {
                self[prop] = event[prop];
            }
        }
        getBacksideText() {
            let text = "";
            text += "<b>Set</b>: " + this.set + "<br/>";
            text += "<b>Type</b>: " + this.type + "<br/>";
            text += "<b>Name</b>: " + this.name + "<br/>";
            text += "(Adversary Event - include only if specified)<br/>";
            text += "Discard and redraw if not playing against " + this.adversary + "<br/>";
            text += this.Inner.getBacksideText();
            text += "<a href=\"https://querki.net/u/darker/spirit-island-faq/#!"
                + encodeURIComponent(this.name[0]) + "\" target='_blank'>FAQ: " + this.name[0] + "</a><br/>";
            return text;
        }
    }
    Types.AdversaryEvent = AdversaryEvent;
    class BlightCard extends Card {
        constructor(set, type, name, blightPerPlayer, effect) {
            super(set, type, name);
            this.name = name;
            this.blightPerPlayer = blightPerPlayer;
            this.effect = effect;
            // set description for searching
            let condition;
            switch (type) {
                case BlightType.BlightedIsland:
                    condition = "If there is ever NO Blight here, players lose.";
                    break;
                case BlightType.StillHealthyIsland:
                    condition = "If there is ever NO Blight here, draw a new Blight Card. It comes into play already flipped.";
                    break;
            }
            this.description = effect + " " + blightPerPlayer + " Blight per player. Any Blight removed from the board returns here. " + condition;
        }
        getImageFolder() {
            return "imgs/blights/";
        }
        getBacksideText() {
            let text = "";
            text += "<b>Set</b>: " + this.set + "<br/>";
            text += "<b>Type</b>: " + this.type + "<br/>";
            text += "<b>Name</b>: " + this.name + "<br/>";
            text += "<b>Effect</b>: " + this.effect + "<br/>";
            text += "<b>Blight per player</b>: " + this.blightPerPlayer + "<br/>";
            text += "<a href=\"https://querki.net/u/darker/spirit-island-faq/#!"
                + encodeURIComponent(this.name) + "\" target='_blank'>FAQ</a><br/>";
            return text;
        }
        getFrontOverlay() {
            return null;
        }
    }
    Types.BlightCard = BlightCard;
})(Types || (Types = {}));
// This file contains material owned by Greater Than Games, LLC.
/// <reference path="types.ts" />
var DB;
(function (DB) {
    var ChoiceEventCard = Types.ChoiceEventCard;
    var ChoiceDesc = Types.ChoiceDesc;
    var ChoiceCost = Types.ChoiceCost;
    var StageEventCard = Types.StageEventCard;
    var TerrorLevelEventCard = Types.TerrorLevelEventCard;
    var HealthyBlightedLandEventCard = Types.HealthyBlightedLandEventCard;
    var EventDesc = Types.EventDesc;
    var AdversaryEvent = Types.AdversaryEvent;
    var Adversary = Types.Adversary;
    var BlightCard = Types.BlightCard;
    var BlightType = Types.BlightType;
    const { PowerCard, ProductSet, Unique, Speed, Ranges, Source, LandAny, Elements, TargetSpirit, TargetProperty, Land, PowerDeckType, FearCard, FearType } = Types;
    let TokenEvent;
    (function (TokenEvent) {
        // Beasts
        // Branch & Claw
        TokenEvent["BeastsAttack"] = "Beasts Attack: Each Beasts deals 2 Damage. Remove any token that destroys Town / City.";
        TokenEvent["BeastsFindNewHomes"] = "Beasts Find New Homes: On Each Board: Push 1 Beasts to an adjacent land without Blight. 1 Fear if Invaders are present there.";
        TokenEvent["BeastsProwl"] = "Beasts Prowl: Each Beasts generates 1 Fear if Invaders are present, and moves to an adjacent land if not.";
        TokenEvent["PreyOnTheUnwary"] = "Prey on the Unwary: Each Beasts destroys 1 Explorer. Add 1 Beasts on a board without one.";
        TokenEvent["SavageFrenzy"] = "Savage Frenzy: Each Beasts destroys 1 Explorer and deals 2 Damage.";
        TokenEvent["BeastsOfTheJungle"] = "Beasts of the Jungle: On Each Board: Add 1 Beasts to a Jungle without Blight. 1 Fear if Invaders are present.";
        TokenEvent["DistantHunt"] = "Distant Hunt: On Each Board: Push 1 Beasts to an adjacent land with no Blight. It deals 1 Damage there.";
        TokenEvent["BeastsProvoked"] = "Beasts Provoked: On Each Board: Add 1 Beasts to a land without Blight that has Town.";
        // Jagged Earth
        TokenEvent["BeastsMultiply"] = "Beasts Multiply: On Each Board: Add 1 Beasts to a land adjacent to Beasts, then Destroy 1 Dahan in a land with Beasts.";
        TokenEvent["CasualtiesOfFangAndSting"] = "Casualties of Fang and Sting: On Each Board: Destroy 1 Explorer / Town in a land with Beasts.";
        TokenEvent["QuitTheFarmedLands"] = "Quit the Farmed Lands: On Each Board: Push 1 Beasts to a land without Town / City. 1 Fear if Explorer are present there.";
        TokenEvent["ExplorersBlunder"] = "Explorers Blunder: On Each Board: Destroy 2 Explorer among lands with Beasts.";
        TokenEvent["PreyOnTheHeedlessJE"] = "Prey on the Heedless: In each land with Beasts, 1 Damage per Beasts.";
        TokenEvent["PreyOnTheHeedlessNI"] = "Prey on the Heedless: In each land with Beasts: 1 Damage per Beasts.";
        TokenEvent["HuntingParties"] = "Hunting Parties: For each land with Beasts and City: 1 Fear and Destroy 1 Beasts there.";
        TokenEvent["BeastsChaseOffHomesteaders"] = "Beasts Chase Off Homesteaders: On Each Board: Push up to 2 Explorer or 1 Town from a land with Beasts.";
        TokenEvent["TerrifyingBeasts"] = "Terrifying Beasts: 2 Fear per board with 2 or more Beasts.";
        TokenEvent["LairInUntamedLands"] = "Lair in Untamed Lands: On Each Board: Add 1 Beasts to a land without Town / City / Blight.";
        TokenEvent["BeastsPreyOnTheInjured"] = "Beasts Prey on the Injured: This turn, Beasts also count as Badlands. On Each Board: Destroy a Damaged Invader in a land with Beasts.";
        // Nature Incarnate
        TokenEvent["TerritorialBeasts"] = "Territorial Beasts: On Each Board: Isolate a land with Beasts. 1 Fear if Invaders are present.";
        TokenEvent["SandStalkers"] = "Sand Stalkers: On Each Board: Add 1 Beasts to the Sands with the most Invaders. 1 Fear if Invaders are present there.";
        // Disease
        // Branch & Claw
        TokenEvent["NewDiseases"] = "New Diseases: On half of the boards (rounding up) add 1 Disease to a land with both Dahan and Invaders. Do 2 Damage to Dahan there.";
        TokenEvent["LingeringPlagues"] = "Lingering Plagues: On Each Board: Add 1 Disease. Disease doesn't prevent Builds this Invader Phase.";
        TokenEvent["WheezelungOutbreak"] = "Wheezelung Outbreak: On Each Board: Add Disease to the Jungle / Wetland with the most Town / City (minimum 1).";
        TokenEvent["GrimToll"] = "Grim Toll: On Each Board: Choose a land with Disease. In that land, do 2 Damage to Invaders and 2 Damage to Dahan.";
        TokenEvent["SandfeverOutbreak"] = "Sandfever Outbreak: On Each Board: Add 1 Disease to the Sands or Mountains with the most Town / City (minimum 1).";
        TokenEvent["ForeignDiseases"] = "Foreign Diseases: On Each Board, in the land with the most combined Invaders + Dahan (min. 1 of each): Add 1 Disease. 2 Damage to Dahan.";
        // Jagged Earth
        TokenEvent["IrregularOutbreaks"] = "Irregular Outbreaks: Disease doesn't prevent Builds this Invader Phase. 1 Fear per board with Disease.";
        TokenEvent["FatalitiesRise"] = "Fatalities Rise: In each land with Disease, 1 Damage to each Invader and 1 Damage to each Dahan. Remove 1 Disease from each land where this Destroys any Town / City.";
        TokenEvent["PlaguesBringFearAndDeath"] = "Plagues Bring Fear and Death: 1 Fear per board with Disease. On Each Board: 2 Damage to Dahan in a land with Disease.";
        TokenEvent["OutbreaksShift"] = "Outbreaks Shift: On Each Board: Push 1 Disease to the adjacent land with the most Invaders (min. 1).";
        TokenEvent["VirulenceAmongClosePackedHomes"] = "Virulence Among Close-Packed Homes: On Each Board: Add 1 Disease to the Inland land with the most Town / City (min. 1).";
        TokenEvent["PestilenceArrivesOnCanvasSails"] = "Pestilence Arrives on Canvas Sails: On Each Board: Add 1 Disease to the Coastal land with the most Town / City (min. 1). In that land, 3 Damage to Dahan.";
        // Nature Incarnate
        TokenEvent["PlaguesInPopulousLands"] = "Plagues in Populous Lands: On Each Board: Add 1 Disease to a land with 3 or more Invaders.";
        // Disease / Strife
        // Branch & Claw
        TokenEvent["Stricken"] = "Stricken: In lands with Disease / Strife, Invaders skip Ravage Actions.";
        // Badlands
        // Nature Incarnate
        TokenEvent["EcosystemDamage"] = "Ecosystem Damage: On Each Board: Add 1 Badlands to a land with Blight.";
        // Badlands / Beasts
        // Nature Incarnate
        TokenEvent["DangerousLands"] = "Dangerous Lands: On Each Board: 1 Damage in a land with Badlands / Beasts. 1 Damage to Dahan in a land with Badlands / Beasts and Dahan.";
        TokenEvent["SecureSettledTerritory"] = "Secure Settled Territory: On Each Board: In a land with Badlands / Beasts and Town / City: Destroy 1 Badlands / Beasts. 1 Damage to Dahan. 1 Damage.";
    })(TokenEvent = DB.TokenEvent || (DB.TokenEvent = {}));
    let DahanEvent;
    (function (DahanEvent) {
        // Branch & Claw
        DahanEvent["CannyDefense"] = "Canny Defense: During Ravage, in every land, Defend 1 per Dahan in the land.";
        DahanEvent["OfferingsOfPatternAndDance"] = "Offerings of Pattern and Dance: Each Spirit with at least 2 Dahan among all its lands gains 1 Energy.";
        DahanEvent["ReclaimTerritory"] = "Reclaim Territory: Each player may Push 1 Dahan to an adjacent land, doing 1 Damage there.";
        DahanEvent["SpiritSpeakersSolveRiddlesOfPower"] = "Spirit-Speakers Solve Riddles of Power: Each Spirit with at least 4 Dahan among its lands gains a Minor Power.";
        DahanEvent["RaidsInForce"] = "Raids in Force: Each Spirit chooses a different land where Dahan outnumber Town / City. Each Dahan there does 1 Damage.";
        DahanEvent["SeekASaferHome"] = "Seek a Safer Home: On Each Board: Push 2 Dahan from a land with Beasts / Disease / Wilds to a land without any of these tokens.";
        DahanEvent["ForsakeTheBarrenLand"] = "Forsake the Barren Land: On Each Board: Push 2 Dahan from a land with Blight to a land without Blight.";
        DahanEvent["Retreat"] = "Retreat: On Each Board: Push 2 Dahan from a land with City to a land without City.";
        DahanEvent["TendTheLand"] = "Tend the Land: On Each Board: Remove 1 Blight from a land with at least 2 Dahan.";
        DahanEvent["ComingOfAgeMountainSands"] = "Coming of Age: On Each Board: Add 1 Dahan to a Mountain or Sands with Dahan.";
        DahanEvent["ComingOfAgeCoastal"] = "Coming of Age: On Each Board: Add 1 Dahan to a Coastal land with Dahan.";
        DahanEvent["ComingOfAgeInland"] = "Coming of Age: On Each Board: Add 1 Dahan to an Inland land with Dahan.";
        DahanEvent["ComingOfAgeJungleWetland"] = "Coming of Age: On Each Board: Add 1 Dahan to a Jungle or Wetland with Dahan.";
        DahanEvent["ComingOfAge2Dahan"] = "Coming of Age: On Each Board: Add 1 Dahan to a land with 2 or more Dahan.";
        DahanEvent["ComingOfAgeNoToken"] = "Coming of Age: On Each Board: Add 1 Dahan to a land with Dahan and no Badlands / Beasts / Disease / Wilds.";
        DahanEvent["ComingOfAgeNoBlightDisease"] = "Coming of Age: On Each Board: Add 1 Dahan to a land with Dahan and no Blight / Disease.";
        DahanEvent["RecklessOffensive"] = "Reckless Offensive: On Each Board: Choose a land with at least 2 Dahan and at least 2 Town / City. Each Dahan destroys 1 Town / City. Add 1 Blight.";
        DahanEvent["RouseTheSpirits"] = "Rouse the Spirits: Each Spirit with at least 3 Dahan among all its lands may use a Slow Power now (instead of later).";
        DahanEvent["FierceMien"] = "Fierce Mien: 1 Fear per land with Invaders where Dahan outnumber Town / City.";
        DahanEvent["TrapsAndSnares"] = "Traps and Snares: On Each Board: Add 1 Wilds to a land with Dahan.";
        DahanEvent["DriveOffTheInterlopers"] = "Drive off the Interlopers: Each player may Push 1 Explorer / Town from a land with Dahan.";
        DahanEvent["AidTheUprising"] = "Aid the Uprising: Invaders with Strife take 1 Damage per Dahan present. Add 1 Dahan per Town / City this destroys.";
        // Jagged Earth
        DahanEvent["CoordinatedDefense"] = "Coordinated Defense: When Invaders Ravage, if the land has both Dahan and Presence, Defend 5.";
        DahanEvent["EngageOnTheirOwnTerms"] = "Engage on Their Own Terms: During Ravage, Dahan only do 1 Damage each, but deal Damage before Invaders.";
        DahanEvent["CleverCooperation"] = "Clever Cooperation: Each Spirit may Push 1 of their Presence from a land with Dahan. 2 Damage in the land Pushed to.";
        DahanEvent["OfferingsOfStoryAndSeason"] = "Offerings of Story and Season: Each Spirit with at least 3 Dahan among all its lands gains 1 Energy and may Reclaim 1 Card.";
        DahanEvent["AThousandSmallStruggles"] = "A Thousand Small Struggles: On Each Board with 4 or more Town / City and 4 or fewer Dahan: Add 1 Blight to a land without Dahan.";
        DahanEvent["SeekOutNewGrounds"] = "Seek Out New Grounds: On Each Board: Gather 1 or 2 Dahan into a land without Dahan Setup symbols.";
        DahanEvent["CarefulDefense"] = "Careful Defense: When Invaders Ravage, if the land has Dahan, Defend 2.";
        DahanEvent["SettlersEncroachTooFar"] = "Settlers Encroach Too Far: On Each Board: Choose a land with Town and Dahan. Push 1 Town per 2 Dahan there.";
        DahanEvent["AtTheirGatesDemandingRedress"] = "At Their Gates Demanding Redress: 2 Fear per land with Dahan and City.";
        DahanEvent["LeaveTheHostileLand"] = "Leave The Hostile Land: In each land, Push 1 Dahan per Badlands / Disease to lands without Badlands / Disease.";
        DahanEvent["SpeakOfTheSpiritsAnger"] = "Speak of the Spirits' Anger: For each board, 1 Fear if any Dahan are in lands with Town / City.";
        DahanEvent["LayAmbushes"] = "Lay Ambushes: During Ravage, Dahan deal Damage at the same time as Invaders.";
        DahanEvent["BlessingsOfBountyAndHealth"] = "Blessings of Bounty and Health: Each Spirit may add 1 Dahan to one of its lands with Dahan.";
        DahanEvent["RaidingAndRetaliation"] = "Raiding and Retaliation: In each land with Town / City: 1 Damage per Dahan, then each surviving Town / City deals 1 Damage to Dahan. (Defend / Strife apply normally.)";
        DahanEvent["CoordinatedStrikes"] = "Coordinated Strikes: In each land with 3 or more Dahan, 2 Damage and Defend 2.";
        DahanEvent["RallyToTheDefenseOfDistantKin"] = "Rally to the Defense of Distant Kin: On Each Board: Gather 1 Dahan into a land with Dahan. In that land, Defend 1 per Dahan.";
        DahanEvent["TellTheOldStories"] = "Tell the Old Stories: Each Spirit with at least 2 Dahan among its lands either Reclaims 1 Power Card or re-gains a Unique Power it previously Forgot.";
        DahanEvent["ReturnToOldPillars"] = "Return to Old Pillars: On Each Board: Gather 1 or 2 Dahan into a land with Dahan Setup symbols.";
        DahanEvent["KeepFarFromTheLandsOfPlague"] = "Keep Far From the Lands of Plague: On Each Board: Push 3 Dahan from lands with Disease to lands without Disease.";
        // Nature Incarnate
        DahanEvent["TendToTheLivingEarth"] = "Tend to the Living Earth: On Each Board with 5 or more Dahan: Remove 1 Blight in a land with Dahan.";
        DahanEvent["StrengthFromTrade"] = "Strength from Trade: Lands with Dahan have Defend 2. In lands with Town / City and no Dahan, Ravage Actions do +1 Damage.";
        DahanEvent["YearsOfHealthAndHarmony"] = "Years of Health and Harmony: On Each Board with 5 or more Dahan: Add 1 Dahan to the land with the most Dahan.";
        DahanEvent["NetworkOfSupportAndTrade"] = "Network of Support and Trade: When Invaders Ravage, if the land has Dahan, Defend 1 + Defend 1 per adjacent Dahan.";
        DahanEvent["SpreadingConflictPromptsCaution"] = "Spreading Conflict Prompts Caution: On Each Board: Push up to 3 Dahan from a land matching a Ravage card to a land not matching a Ravage card.";
        DahanEvent["WaningSupport"] = "Waning Support: On Each Board with Town / City ...and 5 or fewer Dahan: Destroy 1 Presence. ...and 3 or fewer Dahan: Also: Add 1 Blight to a land with Town / City.";
        DahanEvent["WarAmongTheDahan"] = "War Among the Dahan: On Each Board: In the land with the most Dahan (min. 2), Push half the Dahan (round down).";
    })(DahanEvent = DB.DahanEvent || (DB.DahanEvent = {}));
    class Events {
    }
    // Choice
    // Branch & Claw
    Events.LetThePlantsDieAndTheLandWither = new ChoiceDesc("Let the Plants Die and the Land Wither", null, ["For each board, discard the top Minor Power. If it lacks Water, add 1 Blight to a Sands.",
        "Town, City and Dahan have -1 Health (min. 1) until the end of the turn."]);
    Events.ActToEaseTheDrought = new ChoiceDesc("Act to ease the Drought", new ChoiceCost(4, "player", Elements.Water), ["Each Spirit may add 1 Presence to one of their lands with Dahan."]);
    Events.SpurnTheInvaders = new ChoiceDesc("Spurn the Invaders", null, ["On Each Board: 2 Damage to Dahan in a land with Town / City and Dahan.",
        "On Each Board: Add 1 Blight to a land with at least 2 Town / City.",
        "Town / City have -1 Health (min 1) until the end of the turn."]);
    Events.TeachTheInvaders = new ChoiceDesc("Teach the Invaders", null, ["On Each Board: add 1 Town to a land with Dahan.", "The next normal Ravage becomes a Build (This could be on a future turn.)"]);
    Events.LetTheInvasiveSpeciesBloom = new ChoiceDesc("Let the Invasive Species Bloom", null, ["For each board, discard the top Minor Power. If it is Fast, add 1 Blight to a land with Town / City.",
        "After resolving this card, return it to the Event Deck under the top 2 cards."]);
    Events.TransmuteTheWorstOfTheSpecies = new ChoiceDesc("Transmute the Worst of the Species", new ChoiceCost(4, "player", Elements.Moon), ["1 Fear per player. On Each Board: Add 1 Beasts to a land with Town / City."]);
    Events.AllowTheAttacks = new ChoiceDesc("Allow the Attacks", null, ["For each board, discard the top Major Power. Deal its Energy in Damage to Invaders and the land in the Coastal land with the most Town / City (minimum 1). Defend reduces the Damage to both Invaders and the Land."]);
    Events.HelpRepelTheNewcomers = new ChoiceDesc("Help Repel the Newcomers", new ChoiceCost(1, "player", null), ["Add a Fear Card to the top of the Fear Deck."]);
    Events.LetTheIslandsStrengthRepulseThem = new ChoiceDesc("Let the Island's Strength Repulse Them", null, ["Each SacredSite Pushes 1 Explorer / Town to an adjacent land.", "Remove 1 Blight per player from the Blight Card, returning it to the box."]);
    Events.GuardThemYourselfForWellOrIll = new ChoiceDesc("Guard them Yourself, for Well or Ill", new ChoiceCost(3, "land where you do damage", Elements.Fire), ["In each land with SacredSite and Invaders: Either do 2 Damage. -or- Destroy 1 Presence from each Spirit."]);
    Events.StaySteadyAndSlow = new ChoiceDesc("Stay Steady and Slow", null, ["Discard the Power Card.", "Gain 1 Energy, plus the card's printed Energy cost."]);
    Events.WorkToMatchTheirPace = new ChoiceDesc("Work to Match their Pace", null, ["Pay 3 Energy -or- destroy 2 Presence.", "You may choose to resolve the Power Card now. (Instead of during the Slow Phase.)"]);
    Events.IgnoreTheirContactWithTheDahan = new ChoiceDesc("Ignore their Contact with the Dahan", null, ["For each board, discard the top Minor Power. If it has Sun, Push 1 Explorer from a land with Dahan. Otherwise. replace 1 Dahan with 1 Town.",
        "After resolving this card, return it to the Event Deck under the top 2 cards."]);
    Events.CurseTheTonguesOfTheForeigners = new ChoiceDesc("Curse the Tongues of the Foreigners", new ChoiceCost(4, "player", Elements.Sun), ["Each Spirit adds 1 Disease to a land with City.", "2 Fear per Player.", "During the next normal Ravage, City do +3 Damage."]);
    Events.LetThemRampageUntoDeath = new ChoiceDesc("Let them Rampage unto Death", null, ["Each Beasts destroys 1 Dahan.", "Remove 1 Beasts from each board."]);
    Events.GuideTheMadness = new ChoiceDesc("Guide the Madness", new ChoiceCost(3, "Beasts you decide to keep on the island. (min 3 Energy).", Elements.Animal), ["Remove any number of Beasts.", "Each Spirit may Push 1 Beasts to an adjacent land"]);
    Events.IgnoreTheCuriosity = new ChoiceDesc("Ignore the Curiosity", null, ["Return the top card of the Invader Deck to the box. (Skip cards specially placed during Setup.)", "On Each Board: Add 1 Town to a land without one."]);
    Events.WeaveLiesInTheMindsOfTheirObservers = new ChoiceDesc("Weave Lies in the Minds of their Observers", new ChoiceCost(4, "player", Elements.Air), ["Return the top Fear Card to the Box.", "During the next normal Ravage, each Town / City does +1 Damage."]);
    // Jagged Earth
    Events.LeaveItsStrengthWithTheDahan = new ChoiceDesc("Leave Its Strength With the Dahan", null, ["Dahan have +10 Health this turn.", "In lands with Dahan, Invaders have +1 Health this turn."]);
    Events.WithPatientFocusCraftAGreatWarding = new ChoiceDesc("With Patient Focus Craft a Great Warding", new ChoiceCost(4, "player", Elements.Earth), ["Defend from Spirits is 4 lower per land this turn (min. 0).", "During one future Spirit Phase, players may jointly decide to grant Defend 4 to all lands that turn. (There is a Reminder Card for this.)"]);
    Events.TendToYourOwnStrength = new ChoiceDesc("Tend to Your Own Strength", null, ["Each Spirit gains 1 Energy.", "Discard 1 Minor Power per player from the deck. For each with Plant, Remove 1 Blight from the Blight Card, returning it to the box. For each with Animal, Destroy 1 Dahan in a land with Blight."]);
    Events.ForgeAWebOfMutualSupport = new ChoiceDesc("Forge a Web of Mutual Support", new ChoiceCost(4, "player", Elements.Plant), ["Each Spirit Destroys 1 of their Presence.", "Each Spirit gains 1 permanent Element for the rest of the game. (Choose separately, now.)"]);
    Events.LetDestructionHaveItsDay = new ChoiceDesc("Let Destruction Have Its Day", null, ["On Each Board: Remove 1 Beasts. Add 1 Disease.", "For Each Board: Discard the top Minor Power. If it is Fast, add 1 Blight.", "Invaders and Dahan have -1 Health (min. 1) this turn."]);
    Events.FortifyTheResilienceOfLife = new ChoiceDesc("Fortify the Resilience of Life", new ChoiceCost(4, "Player", Elements.Animal), ["On Each Board: Add 1 Beasts. Remove 1 Disease.", "For Each Board: Discard the top Minor Power. If it is Slow, Remove 1 Blight.", "Invaders and Dahan have +1 Health this turn."]);
    Events.IgnoreTheirInterest = new ChoiceDesc("Ignore Their Interest", null, ["Dahan do not participate in Ravages this turn."]);
    Events.DisplayYourWrathAtThisBetrayal = new ChoiceDesc("Display Your Wrath at This Betrayal", new ChoiceCost(2, "player", Elements.Fire), ["Each Spirit with Dahan in their lands Destroys 1 of them and generates 1 Fear."]);
    Events.ChangeAndHelpThemLearnFromTheEnemy = new ChoiceDesc("Change and Help Them Learn From the Enemy", new ChoiceCost(6, "player", Elements.Air), ["Dahan do not participate in Ravages this turn.", "Each Spirit Forgets a Power Card.", "From next turn on, each Dahan provides Defend 1 in its land. (There is a Reminder Card for this.)"]);
    Events.ActCautiouslyInTheBackground = new ChoiceDesc("Act Cautiously in the Background", null, ["On Each Board: Push up to 2 Dahan.", "On Each Board: Add 1 Town to a land without Town.", "On Each Board: Immediately Ravage in the land with the most Invaders that matches a Ravage Card."]);
    Events.CreateUnnervingDistractions = new ChoiceDesc("Create Unnerving Distractions ...at the cost of piquing their interest.", null, ["Ravage Cards skip up to one matching land on each board. (Players choose which.)", "1 Fear per player.", "Remove the bottommost Stage II and Stage III Cards in the Invader Deck from the game."]);
    Events.DrawStrengthFromItWhileYouCan = new ChoiceDesc("Draw Strength From It While You Can", null, ["Remove 1 Blight per player from the Blight Card. Then, if the Blight Card has not flipped, keep Removing Blight until it flips. Gain 3 Energy per Blight Removed, divided as evenly as possible among all Spirits."]);
    Events.PourYourStrengthIntoTheIsland = new ChoiceDesc("Pour Your Strength Into the Island", null, ["Each Spirit either pays 3 Energy, Forgets 2 Power Cards, or returns 1 Presence to their Presence tracks.", "Add 1 Blight per Spirit to the Blight Card (From the box)."]);
    // Nature Incarnate
    Events.EndureItsForcesAsBestYouCan = new ChoiceDesc("Endure Its Forces As Best You Can", null, ["Destroy 1 Presence and lose 1 Energy."]);
    Events.SeekToControlItThoughItExhaustsYou = new ChoiceDesc("Seek To Control It, Though It Exhausts You", null, ["Choose any non-Major Power Card of yours (in hand, play, or discard). Put it into play (without paying its cost); use it immediately (even if already used this turn); and then Forget it.", "Discard all Power Cards (from hand)."]);
    Events.EncourageTheDestruction = new ChoiceDesc("Encourage the Destruction", null, ["4 Fear. Destroy half of Town (round up) and half of City (round up). Add 2 Blight without cascading."]);
    Events.BluntTheOffensive = new ChoiceDesc("Blunt the Offensive", null, ["Destroy 1 Town but do not gain Fear."]);
    Events.LetTheWarningWaftIntoDaysPast = new ChoiceDesc("Let the Warning waft into Days Past", null, ["Lose 1 Energy and replace your most expensive non-Unique Power Card in hand or discard pile (combined) with one of the same type: Reveal the top 4 cards of the deck, Take 1, put it where your card is, then put your card in that deck's discard."]);
    Events.HeadOffTheProblemsYourself = new ChoiceDesc("Head off the Problems Yourself", null, ["Add 1 Omen token (Scenario Marker) to the land without Omens that has the most Invaders (min. 1). After the Ravage Step next turn, at each Omen: 2 Fear. Invaders Ravage. Remove 1 Omen."]);
    // Stage Events
    // Branch & Claw
    Events.SeekingTheInterior = new EventDesc("Seeking the Interior", "In each Coastal land, Push 1 Explorer one land Inland.");
    Events.LocalDiaspora = new EventDesc("Local Diaspora", "In the single land with the most Invaders, Push 1 Explorer / Town to each adjacent land.");
    Events.WaveOfReconnaissance = new EventDesc("Wave of Reconnaissance", "When Exploring: Add 1 additional Explorer to each land Explored.");
    Events.Urbanization = new EventDesc("Urbanization", "In each land with at least 2 Town, replace half the Town (rounding up) with City.");
    Events.InterestingDiscoveries = new EventDesc("Interesting Discoveries", "On Each Board: Choose a SacredSite. Gather 1 Explorer into its land, and add 1 additional Explorer.");
    Events.IncreasingAggression = new EventDesc("Increasing Aggression", "Invaders do +1 Damage (per land) when Ravaging.");
    Events.StrangeTalesAttractExplorers = new EventDesc("Strange Tales attract Explorers", "Now: 1 Fear per Spirit that has at least 1 SacredSite. After advancing Invader Cards: Add 1 Explorer to each land with SacredSite.");
    Events.Fortification = new EventDesc("Fortification", "After advancing Invader Cards: Invaders Build in one terrain not shown under any Invader Action. (If there's no such terrain, nothing happens.)");
    Events.SmallUprising = new EventDesc("Small Uprising", "On Each Board: add 1 Strife to 1 Town. After finishing this Event Card, draw another one, then return this card to the Event Deck as per Setup.");
    Events.Rebellion = new EventDesc("Rebellion!", "On Each Board: Destroy 1 Town. Add 1 Strife to any 2 Town / City. Then, every Invader takes 1 Damage per Strife it has. After finishing this Event card, draw another one. This card is discarded.");
    // Jagged Earth
    Events.InvestedAristocracy = new EventDesc("Invested Aristocracy", "After the Ravage Step, On Each Board where it added no Blight: Add 1 Town to the highest-numbered land with no Invaders.");
    Events.ForeignDignitariesVisit = new EventDesc("Foreign Dignitaries Visit", "If the island is Healthy, Ravages do +2 Damage (total) in the lowest-numbered matching land on each board. If the island is Blighted, add 1 Fear Card to the top of the Fear Deck.");
    Events.SmallerPortsSpringUp = new EventDesc("Smaller Ports Spring Up", "On Each Board with exactly 1 Coastal City: Add 1 Town to a Coastal land without City.");
    Events.ExtensiveBuilding = new EventDesc("Extensive Building", "On Each Board: Build in a land with Invaders not matching a Build Card.");
    Events.HarvestBountyHarvestDust = new EventDesc("Harvest Bounty, Harvest Dust", "If the island is Healthy, On Each Board: Choose a land with Town / City. Ravage there. If the island is Blighted, On Each Board: Push 1 Town from a land with 2 or more Town / City to a land without Town / City.");
    Events.WidespreadClearcutting = new EventDesc("Widespread Clearcutting", "On Each Board: Choose a land with Town / City. Add 1 Blight there, without cascading. Players may destroy 2 Presence / Dahan in that land to prevent adding Blight.");
    Events.NoBraveryWithoutNumbers = new EventDesc("No Bravery without Numbers", "Invaders do not Ravage in lands unless there are more Invaders than the current Terror Level.");
    Events.CourageOfTheCrowd = new EventDesc("Courage of the Crowd", "Invaders do not Ravage in lands unless there are more Invaders than the current Terror Level. Ravage actions do +2 Damage (per land).");
    Events.MapmakersChartTheWild = new EventDesc("Mapmakers Chart the Wild", "Ignore Wilds during the Explore Step. On Each Board without Wilds: Explore Actions add +1 Explorer (in each land successfully Explored).");
    // Terror Level
    // Branch & Claw
    Events.CulturalAssimilation = new EventDesc("Cultural Assimilation", "On Each Board: In a land with exactly 1 Dahan that has or is adjacent to a City, replace that Dahan with 1 Town.");
    Events.ReprisalAgainstTheDahan = new EventDesc("Reprisal Against the Dahan", "On Each Board: choose a land with Dahan and Town / City. Invaders do 3 Damage to Dahan there, ignoring Defend Powers.");
    Events.InvestigationOfDangers = new EventDesc("Investigation of Dangers", "On Each Board: Add 1 Explorer to a land without Invaders or Dahan.");
    Events.DestroyTheUnnatural = new EventDesc("Destroy the unnatural!", "Invaders do +3 Damage (per land) when Ravaging in lands with Presence.");
    Events.DistantExploration = new EventDesc("Distant Exploration", "During the Explore step, Invaders Explore at +1 distance. (So a land 2 away from a Town / City / Ocean will be Explored into.)");
    Events.FearfulMobs = new EventDesc("Fearful Mobs", "When Ravaging, Invaders do +3 Damage (per land) in lands with 3 or more Invaders.");
    // Jagged Earth
    Events.TemporaryTruce = new EventDesc("Temporary Truce", "In lands with Dahan: 1 Dahan and 1 Town / City do not participate in Ravages. (They neither take nor deal Damage.)");
    Events.TemporaryCaution = new EventDesc("Temporary Caution", "During the Ravage Step, On Each Board: Skip 1 Ravage Action in a land where Dahan outnumber Town / City.");
    Events.ResourcefulPopulace = new EventDesc("Resourceful Populace", "For the rest of this turn, after an Action Destroys 1 or more Town / City, add 1 Town to an adjacent land. (If there are no adjacent lands - e.g., due to Isolate - don't add anything.)");
    Events.StripTheLandBare = new EventDesc("Strip the Land Bare", "Town each do +1 Damage when Ravaging. After a Ravage Action adds Blight, Remove 1 Explorer and 1 Town from the Ravaged land.");
    Events.PullTogetherInAdversity = new EventDesc("Pull Together in Adversity", "For the rest of this turn, ignore 1 Strife on each Invader. (This includes not removing that Strife.)");
    Events.PurgeTheLandWithSaltAndFire = new EventDesc("Purge the Land with Salt and Fire", "On Each Board in a land with 2 or more Town: Add 1 Blight without cascading. Add 2 Badlands. Remove all Town.");
    Events.EagerExplorers = new EventDesc("Eager Explorers", "On Each Board: After the first successful Build Action, add 1 Explorer to an adjacent land without Invaders.");
    Events.Xenophobia = new EventDesc("Xenophobia", "When Ravaging in lands with Dahan, each individual Invader does -1 Damage to the land and +1 Damage to Dahan.");
    Events.RelentlessOptimism = new EventDesc("Relentless Optimism", "For the rest of this turn, don't generate Fear for Destroying Town / City.");
    Events.CulturesMixAndClash = new EventDesc("Cultures Mix and Clash", "On Each Board: If Dahan outnumber Town / City by 2 or more, Replace 1 Town with 1 Dahan. If Town / City outnumber Dahan by 2 or more, Replace 1 Dahan with 1 Town.");
    Events.Overconfidence = new EventDesc("Overconfidence", "If you have any Earned Fear Cards, discard 2 of them now (so you don't get their text benefits). Otherwise, move 2 Earned Fear Markers per player to the top of the Fear pool.");
    Events.TerrorBreedsAggression = new EventDesc("Terror Breeds Aggression", "For every 2 Fear Cards currently in the Earned Fear Cards pile, Invaders do +1 Damage (per land) when Ravaging.");
    Events.BureaucratsAdjustFunding = new EventDesc("Bureaucrats Adjust Funding", "On Each Board with 9 or more Town / City: Build Cards skip the highest-numbered matching land. On Each Board with 3 or fewer Town / City: Build Cards cause 1 extra Build Action in the highest-numbered matching land. (This can affect a land without Invaders.)");
    Events.RansackAndRun = new EventDesc("Ransack and Run", "After the Ravage Step, On Each Board: In the land with the most City (min 1), Ravage, then remove 1 City.");
    // Nature Incarnate
    Events.AnOminousDawn = new EventDesc("An Ominous Dawn", "1 Fear per Power Card in play that generates Fear. (In its instructions, not by destroying Town / City. Count thresholds even if you don't have the Elements. Generated Fear can't cause Wavering Resolve.)");
    Events.WaveringResolve = new EventDesc("Wavering Resolve", "Remove 1 Health worth of Invaders per Power Card in play that generates Fear. (In its instructions, not by destroying Town / City. Count thresholds even if you don't have the Elements.)");
    Events.TerrorSpikesUpwards = new EventDesc("Terror Spikes Upwards", "If you have any Earned Fear Cards, resolve the first one now as if the Terror Level were 1 higher (then discard it). Otherwise, 1 Fear per player. (Generated Fear can't cause Final Harvest.)");
    Events.FinalHarvest = new EventDesc("Final Harvest", "Each City does +3 Damage during Ravage Actions. After each Ravage Action, Remove 1 Town / City from that land.");
    // Healthy / Blighted Land
    // Branch & Claw
    Events.PuttingDownRoots = new EventDesc("Putting down Roots", "On an Inland Land on Each Board: Replace 1 Explorer with 1 Town.");
    Events.TheCenterCrumbles = new EventDesc("The Center Crumbles", "On Each Board With Invaders: Add 1 Blight to an Inland land. Spirits may prevent this on any / all boards by destroying 3 Presence from each board to be protected.");
    Events.SearchForNewLands = new EventDesc("Search for new Lands", "In Each Land With at least 2 Explorer: Push 1 Explorer to an adjacent land without Invaders.");
    Events.DevastatedShores = new EventDesc("Devastated Shores", "On Each Board With Invaders: Add 1 Blight to a Coastal land. Spirits may prevent this on any / all boards by destroying 2 Presence from each board to be protected.");
    Events.InvadersSurgeInland = new EventDesc("Invaders Surge Inland", "On a Coastal land on Each Board: Move 1 Town one or two lands inland.");
    Events.WideningDestruction = new EventDesc("Widening Destruction", "On Each Board: add 1 Blight to a land with / adjacent to Town / City. Spirits may prevent this on any / all boards by destroying 2 Presence from each board to be protected.");
    Events.TightKnitCommunities = new EventDesc("Tight-Knit Communities", "For the rest of this turn, Town / City have +1 Health.");
    Events.BlightSpreads = new EventDesc("Blight Spreads", "On Each Board: Add 1 Blight to a land adjacent to a land with Blight. Spirits may prevent this on any / all boards by destroying 2 Presence from each board to be protected.");
    Events.WellPreparedExplorers = new EventDesc("Well-Prepared Explorers", "For the rest of this turn, Explorer have +1 Health.");
    Events.PopulationRises = new EventDesc("Population Rises", "On Each Board: Add 1 Town to a land with Explorer / Town.");
    Events.PowerFades = new EventDesc("Power Fades", "Each Spirit chooses independently to: Destroy 2 of their Presence, -or- Forget 2 of their Powers, -or- Take 1 Blight from the Blight Card and remove it from the game.");
    Events.UrbanDevelopment = new EventDesc("Urban Development", "During the next normal Ravage, each City does +2 Damage. (If there is no Ravage this phase, leave this card by the Ravage space until one happens.)");
    Events.FesteringPitsOfBlight = new EventDesc("Festering Pits of Blight", "On Each Board With Invaders: Add 1 Blight to a land with at least 2 Blight, but do not cascade.");
    Events.HeavyFarming = new EventDesc("Heavy Farming", "During the next normal Ravage, each Town does +1 Damage. (If there is no Ravage this phase, leave this card by the Ravage space until one happens.)");
    Events.OvercrowdedCities = new EventDesc("Overcrowded Cities", "On Each Board with City: Add 1 Blight to a land with City. Spirits may prevent this on any / all boards by destroying 2 Presence from each board to be protected.");
    Events.PromisingFarmland = new EventDesc("Promising Farmland", "When Exploring, once per board, place 1 Town instead of 1 Explorer.");
    Events.NewCashCropsTakeHold = new EventDesc("New Cash Crops Take Hold", "Invaders immediately Ravage in 1 terrain type not showing under any Invader Action. Spirits may prevent this Ravage on any / all boards by destroying 2 Presence from each board to be protected.");
    // Jagged Earth
    Events.ThrivingTrade = new EventDesc("Thriving Trade", "On Each Board: Add 1 City to a Coastal land with City");
    Events.PartitionedWilderness = new EventDesc("Partitioned Wilderness", "On Each Board: If there are 4 or more lands with Town, add 1 Blight to a land with or adjacent to Town. Spirits may prevent this on any/all boards by Destroying 3 Presence from each board to be protected.");
    Events.ProvincialSeat = new EventDesc("Provincial Seat", "On Each Board: Choose a land with City. Build there.");
    Events.LandsHollowOfPromise = new EventDesc("Lands Hollow of Promise", "On Each Board: Add 1 Blight to a land without Presence. Spirits may prevent this on any/all boards by Destroying 2 Presence from each board to be protected.");
    Events.CivicEngagement = new EventDesc("Civic Engagement", "On Each Board: Remove 1 Strife. If you can't, on that board Invaders do +1 Damage (per land) when Ravaging in lands with Town / City.");
    Events.LifesWebTornAsunder = new EventDesc("Life's Web Torn Asunder", "On Each Board with 6 or more Blight: Add 1 Blight to a land adjacent to Blight.");
    Events.WoundedLandsAttractExplorers = new EventDesc("Wounded Lands Attract Explorers", "On Each Board: Add 1 Explorer to a land with Blight.");
    Events.TheWorldsVibranceFades = new EventDesc("The World's Vibrance Fades", "Remove 1 Blight per player from the Blight Card, returning it to the box. Each Spirit may prevent 1 Blight from being Removed by Destroying 2 of their Presence.");
    Events.SeekNewFarmland = new EventDesc("Seek New Farmland", "In each land with 2 or more Town, Push 1 Town to a land without Town.");
    Events.VoraciousConsumption = new EventDesc("Voracious Consumption", "On Each Board: After the Ravage Step, add 1 Blight to a land with City and no Blight. Spirits may prevent this on any/all boards by Destroying 2 Presence from each board to be protected.");
    Events.GradualCorruption = new EventDesc("Gradual Corruption", "On Each Board: Add 1 Blight to a land with Town / City. Spirits may prevent this on any/all boards by paying X Energy per board to protect, where X is the number of cards in the Invader discard. (This may be 0.)");
    Events.RavagedWilderness = new EventDesc("Ravaged Wilderness", "On Each Board: Remove 1 Beasts from a land with Blight. Remove 1 Wilds from a land with Blight.");
    Events.TheFrontierCalls = new EventDesc("The Frontier Calls", "Explore Actions add +1 Explorer to lands without Town / City.");
    Events.SelfSacrificeBuysTime = new EventDesc("Self-Sacrifice Buys Time.", "Destroy 1 Presence from each Spirit. The next X Blight added to the island this turn come from the box instead of the Blight Card, where X is the number of Spirits. (Place this card on the Blight Card as reminder.)");
    Events.FortuneSeekers = new EventDesc("Fortune-Seekers", "The next Explore Card matches all lands without Town / City instead of the printed land type. (you still check for sources of Explorers.) Ignore any Escalation on it.");
    Events.TheLandsBountyExhausted = new EventDesc("The Land's Bounty Exhausted", "In lands without Presence, it only takes 1 Damage to add Blight.");
    Events.CoastalTownMultiply = new EventDesc("Coastal Towns Multiply", "On Each Board: Add 1 Town to a Coastal land adjacent to a Coastal Town.");
    Events.CooperationAmongTowns = new EventDesc("Cooperation Among Towns", "Invaders do +1 Damage (per land) when Ravaging in lands with Town / City and no Strife.");
    Events.CitiesRise = new EventDesc("Cities Rise", "On Each Board: In the land with the most Town, Replace 2 Town with 2 City. (If there is only 1 Town, instead Replace it with 1 City.)");
    Events.DepletedSoil = new EventDesc("Depleted Soil", "In lands with Town / City, it only takes 1 Damage to add Blight.");
    Events.SprawlContainedByTheWilds = new EventDesc("Sprawl Contained by the Wilds", "On Each Board: Add 1 Wilds to a land without Invaders. Build in the land with the most Town / City (min 1).");
    Events.DissolutionThreatens = new EventDesc("Dissolution Threatens", "Spirits are losing awareness and control of pieces of themselves. Each Spirit chooses: ACCEPT THIS FRAGMENTATION: Destroy 2 Presence, adding 1 Wilds in place of each. -or- FOCUS YOUR WILL TOWARDS WHOLENESS: Add 1 of your Destroyed Presence to one of your lands. Next turn, all your Powers are Slow and cannot be made Fast.");
    Events.TheStrugglesOfGrowth = new EventDesc("The Struggles of Growth", "A painful crux-point. Each Spirit chooses: TRADE REACH FOR DEEPER NATURE: Destroy 2 of your Presence. Gain a Power Card. -or- LEAVE BEHIND THAT WHICH RESTRAINS YOU: Forget a Power Card. Gain 2 Energy. Move up to 2 of your Presence up to 4 Range.");
    Events.BlightDeepens = new EventDesc("Blight Deepens", "On Each Board: Add 1 Blight to a land with Blight, but do not cascade. Spirits may prevent this on any/all boards by Destroying 1 Presence from each board to be protected.");
    // Nature Incarnate
    Events.AccumulatedDevastation = new EventDesc("Accumulated Devastation", "On Each Board: During the first successful Ravage Action (in one land) this Invader Phase, increase the total Damage ravaging Invaders deal to each land (but not to Dahan) by the current Invader Stage. Do this for at most one Ravage Action per board (for one Ravage Action in one land).");
    Events.FocusedFarming = new EventDesc("Focused Farming", "On Each Board: Add 1 Explorer and 1 Town to a land with Town / Blight.");
    Events.EssenceDisperses = new EventDesc("Essence Disperses", "Each Spirit chooses independently to: Forget 1 Power Card. -or- Lose 2 Energy (to min. 0) and Destroy 1 Presence. In the land where you destroyed Presence, return 1 Blight to the box (if possible).");
    Events.InfluxOfSettlers = new EventDesc("Influx of Settlers", "On the single board with the most Town / City: Add 1 Town per player, split between as many different lands as possible. (This will usually be 1 Town per chosen land.)");
    Events.LethargyAndDegeneration = new EventDesc("Lethargy and Degeneration", "On Each Board: Skip the first Ravage Action (in one land). Add 1 Blight to a land with Town / City. Spirits may prevent either / both effects on any / all boards (choose per board) by Destroying 2 Presence from each board to be protected.");
    Events.SearchForUnclaimedLand = new EventDesc("Search for Unclaimed Land", "On Each Board: Explore in the land with the fewest total Invaders / Dahan (no source required).");
    Events.WidespreadHunting = new EventDesc("Widespread Hunting", "When Town / City Ravage in a land: If no Beasts are present, Invaders do +2 Damage (total). Otherwise, Destroy 1 Beasts. Do this at most once per board (for one Ravage Action in one land).");
    DB.CARDS = [
        // Spirit Cards
        new PowerCard(ProductSet.Basegame, Unique.LightningsSwiftStrike, "Shatter Homesteads", 2, Speed.Slow, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Fire, Elements.Air], "Rocky Hammer", "1 Fear. Destroy 1 Town."),
        new PowerCard(ProductSet.Basegame, Unique.LightningsSwiftStrike, "Raging Storm", 3, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Fire, Elements.Air, Elements.Water], "Rocky Hammer", "1 Damage to each Invader."),
        new PowerCard(ProductSet.Basegame, Unique.LightningsSwiftStrike, "Lightning's Boon", 1, Speed.Fast, null, TargetSpirit.Any, [Elements.Fire, Elements.Air], "Rocky Hammer", "Target Spirit may use up to 2 Slow Powers as if they were Fast Powers this turn"),
        new PowerCard(ProductSet.Basegame, Unique.LightningsSwiftStrike, "Harbingers of the Lightning", 0, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Fire, Elements.Air], "Rocky Hammer", "Push up to 2 Dahan. 1 Fear if you pushed any Dahan into a land with Town / City"),
        new PowerCard(ProductSet.Basegame, Unique.RiverSurgesInSunlight, "Flash Floods", 2, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Water], "Nolan Nasser", "1 Damage. If target land is Coastal, +1 Damage."),
        new PowerCard(ProductSet.Basegame, Unique.RiverSurgesInSunlight, "Wash Away", 1, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Water, Elements.Earth], "Nolan Nasser", "Push up to 3 Explorer / Town"),
        new PowerCard(ProductSet.Basegame, Unique.RiverSurgesInSunlight, "Boon of Vigor", 0, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Water, Elements.Plant], "Nolan Nasser", "If you target yourself, gain 1 Energy. If you target another Spirit, they gain 1 Energy per Power Card they played this turn."),
        new PowerCard(ProductSet.Basegame, Unique.RiverSurgesInSunlight, "River's Bounty", 0, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Sun, Elements.Water, Elements.Animal], "Nolan Nasser", "Gather up to 2 Dahan. If there are now at least 2 Dahan, add 1 Dahan and gain 1 Energy."),
        new PowerCard(ProductSet.Basegame, Unique.ShadowsFlickerLikeFlame, "Concealing Shadows", 0, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Moon, Elements.Air], "Nolan Nasser", "1 Fear. Dahan take no damage from Ravaging Invaders this turn."),
        new PowerCard(ProductSet.Basegame, Unique.ShadowsFlickerLikeFlame, "Favors Called Due", 1, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Moon, Elements.Air, Elements.Animal], "Nolan Nasser", "Gather up to 4 Dahan. If Invaders are present and Dahan now outnumber them, 3 Fear."),
        new PowerCard(ProductSet.Basegame, Unique.ShadowsFlickerLikeFlame, "Mantle of Dread", 1, Speed.Slow, null, TargetSpirit.Any, [Elements.Moon, Elements.Fire, Elements.Air], "Nolan Nasser", "2 Fear. Target Spirit may Push 1 Explorer and 1 Town from a land where it has Presence."),
        new PowerCard(ProductSet.Basegame, Unique.ShadowsFlickerLikeFlame, "Crops Wither and Fade", 1, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Moon, Elements.Fire, Elements.Plant], "Nolan Nasser", "2 Fear. Replace 1 Town with 1 Explorer. -or- Replace 1 City with 1 Town."),
        new PowerCard(ProductSet.Basegame, Unique.VitalStrengthOfTheEarth, "Guard the Healing Land", 3, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Water, Elements.Earth, Elements.Plant], "Sydni Kruger", "Remove 1 Blight. Defend 4."),
        new PowerCard(ProductSet.Basegame, Unique.VitalStrengthOfTheEarth, "A Year of Perfect Stillness", 3, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Earth], "Sydni Kruger", "Invaders skip all Actions in target land this turn."),
        new PowerCard(ProductSet.Basegame, Unique.VitalStrengthOfTheEarth, "Rituals of Destruction", 3, Speed.Slow, new Ranges(Source.SacredSite, 1), TargetProperty.Dahan, [Elements.Sun, Elements.Moon, Elements.Fire, Elements.Earth, Elements.Plant], "Sydni Kruger", "2 Damage. If target land has at least 3 Dahan, +3 Damage and 2 Fear."),
        new PowerCard(ProductSet.Basegame, Unique.VitalStrengthOfTheEarth, "Draw of the Fruitful Earth", 1, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Earth, Elements.Plant, Elements.Animal], "Sydni Kruger", "Gather up to 2 Explorer. Gather up to 2 Dahan."),
        new PowerCard(ProductSet.Basegame, Unique.Thunderspeaker, "Manifestation of Power and Glory", 3, Speed.Slow, new Ranges(Source.Presence, 0), TargetProperty.Dahan, [Elements.Sun, Elements.Fire, Elements.Air], "Loic Belliau", "1 Fear. Each Dahan deals damage equal to the number of your Presence in target land."),
        new PowerCard(ProductSet.Basegame, Unique.Thunderspeaker, "Words of Warning", 1, Speed.Fast, new Ranges(Source.Presence, 1), TargetProperty.Dahan, [Elements.Sun, Elements.Air, Elements.Animal], "Loic Belliau", "Defend 3. During Ravage, Dahan in target land deal damage simultaneously with Invaders."),
        new PowerCard(ProductSet.Basegame, Unique.Thunderspeaker, "Sudden Ambush", 2, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Fire, Elements.Air, Elements.Animal], "Loic Belliau", "You may Gather 1 Dahan. Each Dahan destroys 1 Explorer."),
        new PowerCard(ProductSet.Basegame, Unique.Thunderspeaker, "Voice of Thunder", 0, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Air], "Loic Belliau", "Push up to 4 Dahan. -or- If Invaders are Present, 2 Fear."),
        new PowerCard(ProductSet.Basegame, Unique.OceansHungryGrasp, "Call of the Deeps", 0, Speed.Fast, new Ranges(Source.Presence, 0), Land.Coastal, [Elements.Moon, Elements.Air, Elements.Water], "Joshua Wright", "Gather 1 Explorer. If target land is the Ocean, you may Gather another Explorer."),
        new PowerCard(ProductSet.Basegame, Unique.OceansHungryGrasp, "Grasping Tide", 1, Speed.Fast, new Ranges(Source.Presence, 1), Land.Coastal, [Elements.Moon, Elements.Water], "Joshua Wright", "2 Fear. Defend 4."),
        new PowerCard(ProductSet.Basegame, Unique.OceansHungryGrasp, "Swallow the Land-Dwellers", 0, Speed.Slow, new Ranges(Source.Presence, 0), Land.Coastal, [Elements.Water, Elements.Earth], "Joshua Wright", "Drown 1 Explorer, 1 Town, and 1 Dahan."),
        new PowerCard(ProductSet.Basegame, Unique.OceansHungryGrasp, "Tidal Boon", 1, Speed.Slow, null, TargetSpirit.Another, [Elements.Moon, Elements.Water, Elements.Earth], "Joshua Wright", "Target Spirit gains 2 Energy and may Push 1 Town and up to 2 Dahan from one of their lands. If Dahan are pushed to your ocean, you may move them to any Coastal land instead of Drowning them."),
        new PowerCard(ProductSet.Basegame, Unique.BringerOfDreamsAndNightmares, "Predatory Nightmares", 2, Speed.Slow, new Ranges(Source.SacredSite, 1), TargetProperty.Invaders, [Elements.Moon, Elements.Fire, Elements.Earth, Elements.Animal], "Shane Tyree", "2 Damage. Push up to 2 Dahan. (When your powers would destroy Invaders, instead they generate Fear and/or Push those Invaders.)"),
        new PowerCard(ProductSet.Basegame, Unique.BringerOfDreamsAndNightmares, "Dread Apparitions", 2, Speed.Fast, new Ranges(Source.Presence, 1), TargetProperty.Invaders, [Elements.Moon, Elements.Air], "Shane Tyree", "When Powers generate Fear in target land, Defend 1 per Fear. 1 Fear. (Fear from To Dream a Thousand Deaths counts. Fear from destroying Town / City does not.)"),
        new PowerCard(ProductSet.Basegame, Unique.BringerOfDreamsAndNightmares, "Call on Midnight's Dream", 0, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Moon, Elements.Animal], "Shane Tyree", "If target land has Dahan, gain a Major Power. If you Forget this Power, gain Energy equal to Dahan and you may play the Major Power immediately, paying its cost. -or- If Invaders are present, 2 Fear."),
        new PowerCard(ProductSet.Basegame, Unique.BringerOfDreamsAndNightmares, "Dreams of the Dahan", 0, Speed.Fast, new Ranges(Source.Presence, 2), LandAny, [Elements.Moon, Elements.Air], "Shane Tyree", "Gather up to 2 Dahan. -or- If target land has Town / City, 1 Fear for each Dahan, to a maximum of 3 Fear."),
        new PowerCard(ProductSet.Basegame, Unique.ASpreadOfRampantGreen, "Overgrow in a Night", 2, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Moon, Elements.Plant], "Jorge Ramos", "Add 1 Presence. -or- If target land has your Presence and Invaders, 3 Fear."),
        new PowerCard(ProductSet.Basegame, Unique.ASpreadOfRampantGreen, "Gift of Proliferation", 1, Speed.Fast, null, TargetSpirit.Another, [Elements.Moon, Elements.Plant], "Jorge Ramos", "Target Spirit adds 1 Presence up to 1 Range from their Presence."),
        new PowerCard(ProductSet.Basegame, Unique.ASpreadOfRampantGreen, "Fields Choked with Growth", 0, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Water, Elements.Plant], "Jorge Ramos", "Push 1 Town. -or- Push 3 Dahan"),
        new PowerCard(ProductSet.Basegame, Unique.ASpreadOfRampantGreen, "Stem the Flow of Fresh Water", 0, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Water, Elements.Plant], "Jorge Ramos", "1 Damage to 1 Town / City. If target land is Mountain / Sands, instead, 1 Damage to each Town / City."),
        // Colored Corners
        // green corner
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Savage Mawbeasts", 0, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Fire, Elements.Animal], "Cari Corene", "If target land is Jungle / Wetland, 1 Fear and 1 Damage. -If you have- 3 Animal: 1 Damage."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Voracious Growth", 1, Speed.Slow, new Ranges(Source.SacredSite, 1), [Land.Jungle, Land.Wetland], [Elements.Water, Elements.Plant], "Cari Corene", "2 Damage. -or- Remove 1 Blight."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Rouse the Trees and Stones", 1, Speed.Slow, new Ranges(Source.SacredSite, 1), TargetProperty.NoBlight, [Elements.Fire, Elements.Earth, Elements.Plant], "Jorge Ramos", "2 Damage. Push 1 Explorer."),
        // blue corner
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Encompassing Ward", 1, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Water, Elements.Earth], "Jorge Ramos", "Target Spirit provides Defend 2 in each of its lands."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Song of Sanctity", 1, Speed.Slow, new Ranges(Source.Presence, 1), [Land.Mountain, Land.Jungle], [Elements.Sun, Elements.Water, Elements.Plant], "Nolan Nasser", "If target land has 1 Explorer, Push all Explorer. Otherwise, remove 1 Blight."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Uncanny Melting", 1, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Sun, Elements.Moon, Elements.Water], "Joshua Wright", "If Invaders are present, 1 Fear. If target land is Sands / Wetland, remove 1 Blight"),
        // red corner
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Shadows of the Burning Forest", 0, Speed.Slow, new Ranges(Source.Presence, 0), TargetProperty.Invaders, [Elements.Moon, Elements.Fire, Elements.Plant], "Nolan Nasser", "2 Fear. If target land is Mountain / Jungle, Push 1 Explorer and 1 Town."),
        // Minors inside color cornered block
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Steam Vents", 1, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Fire, Elements.Air, Elements.Water, Elements.Earth], "Joshua Wright", "Destroy 1 Explorer. -If you have- 3 Earth: You may instead destroy 1 Town."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Veil the Night's Hunt", 1, Speed.Fast, new Ranges(Source.Presence, 2), TargetProperty.Dahan, [Elements.Moon, Elements.Air, Elements.Animal], "Loic Belliau", "Each Dahan deals 1 Damage to a different Invader. -or- Push up to 3 Dahan."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Elemental Boon", 1, Speed.Fast, null, TargetSpirit.Any, [], "Moro Rogers", "Target Spirit gains 3 different Elements of their choice. If you target another Spirit, you also gain the chosen Elements."),
        // Second Badge
        // Minors
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Devouring Ants", 1, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Sun, Elements.Earth, Elements.Animal], "Nolan Nasser", "1 Fear. 1 Damage. Destroy 1 Dahan. If target land is Jungle / Sands, +1 Damage."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Dark and Tangled Woods", 1, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Moon, Elements.Earth, Elements.Plant], "Nolan Nasser", "2 Fear. If target land is Mountain / Jungle, Defend 3."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Sap the Strength of Multitudes", 0, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Water, Elements.Animal], "Loic Belliau", "Defend 5. -If you have- 1 Air: Increase this Power's Range by 1"),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Drift down into Slumber", 0, Speed.Fast, new Ranges(Source.Presence, 2), LandAny, [Elements.Air, Elements.Earth, Elements.Plant], "Lucas Durham", "Defend 1. If target land is Jungle / Sands, instead, Defend 4."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Land of Haunts and Embers", 0, Speed.Fast, new Ranges(Source.Presence, 2), LandAny, [Elements.Moon, Elements.Fire, Elements.Air], "Jorge Ramos", "2 Fear. Push up to 2 Explorer / Town. If target land has Blight, +2 Fear. Push up to 2 more Explorer / Town. Add 1 Blight."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Nature's Resilience", 1, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Earth, Elements.Plant, Elements.Animal], "Joshua Wright", "Defend 6. -If you have- 2 Water: You may instead remove 1 Blight."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Visions of Fiery Doom", 1, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Moon, Elements.Fire], "Lucas Durham", "1 Fear. Push 1 Explorer / Town. -If you have- 2 Fire: +1 Fear."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Pull Beneath the Hungry Earth", 1, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Moon, Elements.Water, Elements.Earth], "Nolan Nasser", "If target land has your Presence, 1 Fear and 1 Damage. If target land is Sands / Wetland, 1 Damage."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Call of the Dahan Ways", 1, Speed.Slow, new Ranges(Source.Presence, 1), TargetProperty.Dahan, [Elements.Moon, Elements.Water, Elements.Animal], "Loic Belliau", "Replace 1 Explorer with 1 Dahan. -If you have- 2 Moon: You may instead replace 1 Town with 1 Dahan."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Call to Bloodshed", 1, Speed.Slow, new Ranges(Source.Presence, 1), TargetProperty.Dahan, [Elements.Sun, Elements.Fire, Elements.Animal], "Jorge Ramos", "1 Damage per Dahan. -or- Gather up to 3 Dahan."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Call to Isolation", 0, Speed.Fast, new Ranges(Source.Presence, 1), TargetProperty.Dahan, [Elements.Sun, Elements.Air, Elements.Animal], "Graham Stermberg", "Push 1 Explorer / Town per Dahan. -or- Push 1 Dahan."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Call to Migrate", 1, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Fire, Elements.Air, Elements.Animal], "Graham Stermberg", "Gather up to 3 Dahan. Push up to 3 Dahan."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Call to Tend", 1, Speed.Slow, new Ranges(Source.Presence, 1), TargetProperty.Dahan, [Elements.Water, Elements.Plant, Elements.Animal], "Loic Belliau", "Remove 1 Blight. -or- Push up to 3 Dahan."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Quicken the Earth's Struggles", 1, Speed.Fast, new Ranges(Source.SacredSite, 0), LandAny, [Elements.Moon, Elements.Fire, Elements.Earth, Elements.Animal], "Lucas Durham", "1 Damage to each Town / City. -or- Defend 10."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Delusions of Danger", 1, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Moon, Elements.Air], "Moro Rogers", "Push 1 Explorer. -or- 2 Fear."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Drought", 1, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Fire, Elements.Earth], "Nolan Nasser", "Destroy 3 Town. 1 Damage to each Town / City. Add 1 Blight. -If you have- 3 Sun: Destroy 1 City."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Gift of Constancy", 0, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Earth], "Moro Rogers", "Target Spirit gains 2 Energy. At end of turn, target Spirit may Reclaim 1 Power Card instead of discarding it. If you target another Spirit, you may also Reclaim 1 Power Card instead of discarding it."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Enticing Splendor", 0, Speed.Fast, new Ranges(Source.Presence, 0), TargetProperty.NoBlight, [Elements.Sun, Elements.Air, Elements.Plant], "Joshua Wright", "Gather 1 Explorer / Town. -or- Gather up to 2 Dahan."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Entrancing Apparitions", 1, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Moon, Elements.Air, Elements.Water], "Moro Rogers", "Defend 2. If no Invaders are present, gather up to 2 Explorer."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Gift of Living Energy", 0, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Fire, Elements.Plant], "Nolan Nasser", "Target Spirit gains 1 Energy, +1 Energy if target Spirit is not yourself. If you have at least 2 SacredSite, target Spirit gains +1 Energy."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Gift of Power", 0, Speed.Slow, null, TargetSpirit.Any, [Elements.Moon, Elements.Water, Elements.Earth, Elements.Plant], "Joshua Wright", "Target Spirit gains a Minor Power Card."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Gnawing Rootbiters", 0, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Earth, Elements.Animal], "Moro Rogers", "Push up to 2 Town."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Lure of the Unknown", 0, Speed.Fast, new Ranges(Source.Presence, 2), TargetProperty.NoInvaders, [Elements.Moon, Elements.Fire, Elements.Air, Elements.Plant], "Lucas Durham", "Gather 1 Explorer / Town"),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Purifying Flame", 1, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Sun, Elements.Fire, Elements.Air, Elements.Plant], "Jorge Ramos", "1 Damage per Blight. If target land is Mountain / Sands, you may instead remove 1 Blight."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Rain of Blood", 0, Speed.Slow, new Ranges(Source.SacredSite, 1), TargetProperty.Invaders, [Elements.Air, Elements.Water, Elements.Animal], "Kat Birmelin", "2 Fear. If target land has at least 2 Town / City, +1 Fear."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Minor, "Reaching Grasp", 0, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Air, Elements.Water], "Nolan Nasser", "Target Spirit gets +2 Range with all their Powers."),
        // Majors
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Accelerated Rot", 4, Speed.Slow, new Ranges(Source.Presence, 2), [Land.Jungle, Land.Wetland], [Elements.Sun, Elements.Water, Elements.Plant], "Graham Stermberg", "2 Fear. 4 Damage. -If you have- 3 Sun, 2 Water, 3 Plant: +5 Damage. Remove 1 Blight."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Cleansing Floods", 5, Speed.Slow, new Ranges(Source.Presence, 1, [Land.Wetland]), LandAny, [Elements.Sun, Elements.Water], "Nolan Nasser", "4 Damage. Remove 1 Blight. -If you have- 4 Water: +10 Damage."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Pillar of Living Flame", 5, Speed.Slow, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Fire], "Jorge Ramos", "3 Fear. 5 Damage. If target land is Jungle / Wetland, add 1 Blight. -If you have- 4 Fire: +2 Fear and +5 Damage."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Poisoned Land", 3, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Earth, Elements.Plant, Elements.Animal], "Nolan Nasser", "1 Fear. 7 Damage. Add 1 Blight and destroy all Dahan. -If you have- 3 Earth, 2 Plant, 2 Animal: For each Blight then present, +1 Fear and +4 Damage."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Terrifying Nightmares", 4, Speed.Fast, new Ranges(Source.Presence, 2), LandAny, [Elements.Moon, Elements.Air], "Loic Belliau", "2 Fear. Push up to 4 Explorer / Town. -If you have- 4 Moon: +4 Fear."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "The Trees and Stones Speak of War", 2, Speed.Fast, new Ranges(Source.Presence, 1), TargetProperty.Dahan, [Elements.Sun, Elements.Earth, Elements.Plant], "Graham Stermberg", "For each Dahan in target land, 1 Damage and Defend 2. -If you have- 2 Sun, 2 Earth, 2 Plant: You may Push up to 2 Dahan, moving each one's Defend with them."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Entwined Power", 2, Speed.Fast, null, TargetSpirit.Another, [Elements.Moon, Elements.Water, Elements.Plant], "Joshua Wright", "You and target Spirit may use each other's Presence to target Powers. Target Spirit gains a Power Card. You gain one of the power Cards they did not keep. -If you have- 2 Water, 4 Plant: You and target Spirit each gain 3 Energy and may gift the other 1 Power from hand."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Paralyzing Fright", 4, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Air, Elements.Earth], "Joshua Wright", "4 Fear. Invaders skip all Actions in target land this turn. -If you have- 2 Air, 3 Earth: +4 Fear."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Powerstorm", 3, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Fire, Elements.Air], "Nolan Nasser", "Target Spirit gains 3 Energy. Once this turn, target may Repeat a Power Card by paying its cost again. -If you have- 2 Sun, 2 Fire, 3 Air: Target may Repeat up to 2 more Power Cards by paying their costs."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Talons of Lightning", 6, Speed.Fast, new Ranges(Source.Presence, 1), [Land.Mountain, Land.Wetland], [Elements.Fire, Elements.Air], "Nolan Nasser", "3 Fear. 5 Damage. -If you have- 3 Fire, 3 Air: Destroy 1 Town in each adjacent land. Increase this power's Range to 3 Range."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "The Jungle Hungers", 3, Speed.Slow, new Ranges(Source.Presence, 1, [Land.Jungle]), LandAny, [Elements.Moon, Elements.Plant], "Joshua Wright", "Destroy all Explorer and all Town. Destroy all Dahan. -If you have- 2 Moon, 3 Plant: Destroy 1 City. Do not destroy any Dahan."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "The Land Thrashes in Furious Pain", 4, Speed.Slow, new Ranges(Source.Presence, 2), TargetProperty.Blight, [Elements.Moon, Elements.Fire, Elements.Earth], "Nolan Nasser", "2 Damage per Blight in target land. +1 Damage per Blight in adjacent lands. -If you have- 3 Moon, 3 Earth: Repeat on an adjacent land."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Tsunami", 6, Speed.Slow, new Ranges(Source.SacredSite, 2), Land.Coastal, [Elements.Water, Elements.Earth], "Jason Behnke", "2 Fear. 8 Damage. Destroy 2 Dahan. -If you have- 3 Water, 2 Earth: In each other Coastal land on the same board: 1 Fear, 4 Damage, and Destroy 1 Dahan."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Vigor of the Breaking Dawn", 3, Speed.Fast, new Ranges(Source.Presence, 2), TargetProperty.Dahan, [Elements.Sun, Elements.Animal], "Loic Belliau", "2 Damage per Dahan in target land. -If you have- 3 Sun, 2 Animal: You may Push up to 2 Dahan. In lands you Pushed Dahan to, 2 Damage per Dahan."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Vengeance of the Dead", 3, Speed.Fast, new Ranges(Source.Presence, 3), LandAny, [Elements.Moon, Elements.Fire, Elements.Animal], "Kat Birmelin", "3 Fear. After each effect that destroys Town / City / Dahan in target land, 1 Damage per Town / City / Dahan destroyed. -If you have- 3 Animal: Damage from this Power may be dealt into adjacent lands."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Wrap in Wings of Sunlight", 3, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Sun, Elements.Air, Elements.Animal], "Loic Belliau", "Move up to 5 Dahan from target land to any land. Defend 5 in that land. -If you have- 2 Sun, 2 Air, 2 Animal: First, Gather up to 3 Dahan."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Blazing Renewal", 5, Speed.Fast, null, TargetSpirit.Any, [Elements.Fire, Elements.Earth, Elements.Plant], "Nolan Nasser", "Target Spirit adds 2 of their destroyed Presence into a single land, up to 2 Range from your Presence. If any Presence was added, 2 damage to each Town / City in that land. -If you have- 3 Fire, 3 Earth, 2 Plant: 4 Damage in that land."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Winds of Rust and Atrophy", 3, Speed.Fast, new Ranges(Source.SacredSite, 3), LandAny, [Elements.Air, Elements.Water, Elements.Animal], "Joshua Wright", "1 Fear and Defend 6. Replace 1 City with 1 Town or 1 Town with 1 Explorer. -If you have- 3 Air, 3 Water, 2 Animal: Repeat this Power."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Indomitable Claim", 4, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Earth], "Jorge Ramos", "Add 1 Presence in target land even if you normally could not due to land type. Defend 20. -If you have- 2 Sun, 3 Earth: 3 Fear if Invaders are present. Invaders skip all Actions in target land this turn."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Mists of Oblivion", 4, Speed.Slow, new Ranges(Source.Presence, 3), LandAny, [Elements.Moon, Elements.Air, Elements.Water], "Nolan Nasser", "1 Fear per Town / City this Power destroys (to a maximum of 4). 1 Damage to each Invader. -If you have- 2 Moon, 3 Air, 2 Water: 3 Damage."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Infinite Vitality", 3, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Earth, Elements.Plant, Elements.Animal], "Joshua Wright", "Dahan have +4 Health while in target land. Whenever Blight would be added to target land, instead leave it on the card. -If you have- 4 Earth: Dahan ignore Damage and Destruction effects. Remove 1 Blight from target or adjacent land."),
        new PowerCard(ProductSet.Basegame, PowerDeckType.Major, "Dissolve the Bonds of Kinship", 4, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Fire, Elements.Water, Elements.Animal], "Jorge Ramos", "Replace 1 City with 2 Explorer. Replace 1 Town with 1 Explorer. Replace 1 Dahan with 1 Explorer. Push all Explorer from target land to as many different lands as possible. -If you have- 2 Fire, 2 Water, 3 Animal: Before Pushing, Explorer and Town / City do Damage to each other."),
        // Branch & Claw
        // Majors
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Strangling Firevine", 4, Speed.Slow, new Ranges(Source.Presence, 1, [Land.Sands]), LandAny, [Elements.Fire, Elements.Plant], "Nolan Nasser", "Destroy all Explorer. Add 1 Wilds. Add 1 Wilds in the originating Sands. 1 Damage per Wilds in / adjacent to target land. -If you have- 2 Fire, 3 Plant: +1 Damage per Wilds in / adjacent to target land."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Bloodwrack Plague", 4, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Water, Elements.Earth, Elements.Animal], "Jorge Ramos", "Add 2 Disease. For each Disease in target land, Defend 1 in target and all adjacent lands. -If you have- 2 Earth, 4 Animal: 2 Fear. For each Disease in target land do 1 Damage in target or an adjacent land."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Cast down into the Briny Deep", 9, Speed.Slow, new Ranges(Source.SacredSite, 1), [Land.Coastal], [Elements.Sun, Elements.Moon, Elements.Water, Elements.Earth], "Jason Behnke", "6 Fear. Destroy all Invaders. -If you have- 2 Sun, 2 Moon, 4 Water, 4 Earth: Destroy the board containing target land and everything on that board. All destroyed Blight is removed from the game instead of being returned to the Blight Card."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Death Falls Gently from Open Blossoms", 4, Speed.Slow, new Ranges(Source.Presence, 3), [Land.Jungle, Land.Sands], [Elements.Moon, Elements.Air, Elements.Plant], "Graham Stermberg", "4 Damage. If any Invaders remain, add 1 Disease. -If you have- 3 Air, 3 Plant: 3 Fear. Add 1 Disease to 2 adjacent lands with Invaders."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Fire and Flood", 7, Speed.Slow, new Ranges(Source.SacredSite, [1, 2]), LandAny, [Elements.Sun, Elements.Fire, Elements.Water], "Jason Behnke", "4 Damage in each target land. (Range must be measured from the same SacredSite.) -If you have- 3 Fire: +4 Damage in either target land. 3 Water: +4 Damage in either target land."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Grant Hatred a Ravenous Form", 4, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Moon, Elements.Fire], "Nolan Nasser", "For each Strife / Blight in target land, 1 Fear and 2 Damage. If this destroys all invaders in target land, add 1 Beasts. -If you have- 4 Moon, 2 Fire: Add 1 Strife in up to 3 adjacent lands."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Insatiable Hunger of the Swarm", 4, Speed.Fast, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Air, Elements.Plant, Elements.Animal], "Lucas Durham", "Add 1 Blight. Add 2 Beasts. Gather up to 2 Beasts. Each Beasts deal 1 Fear, 2 Damage to Invaders and 2 Damage to Dahan. Destroy 1 Beasts. -If you have- 2 Air, 4 Animal: Repeat this Power on an adjacent land."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Instruments of their own Ruin", 4, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Sun, Elements.Fire, Elements.Air, Elements.Animal], "Lucas Durham", "Add 1 Strife. Each Invader with Strife deals Damage to other Invaders in target land. -If you have- 4 Sun, 2 Fire, 2 Animal: Instead, if Invaders Ravage in target land, they damage Invaders in adjacent lands instead of Dahan and the land. Dahan in target land do not fight back."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Flow like Water, Reach like Air", 2, Speed.Fast, null, TargetSpirit.Any, [Elements.Air, Elements.Water], "Joshua Wright", "Target Spirit gets +2 Range with all Powers. Target Spirit may Push 1 of their Presence to an adjacent land, bringing up to 2 Explorer, 2 Town and 2 Dahan along with it. -If you have- 2 Air, 2 Water: The moved Presence may also bring along up to 2 City and up to 2 Blight."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Pent-Up Calamity", 3, Speed.Fast, new Ranges(Source.Presence, 2), LandAny, [Elements.Moon, Elements.Fire, Elements.Earth, Elements.Plant, Elements.Animal], "Joshua Wright", "Add 1 Disease and 1 Strife. -or- Remove any number of Beasts / Disease / Strife / Wilds. For each token removed, 1 Fear and 3 Damage. -If you have- 2 Moon, 3 Fire: If you have removed tokens, return up to 2 of them. Otherwise, add 2 Strife."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Pyroclastic Flow", 3, Speed.Fast, new Ranges(Source.Presence, 1, [Land.Mountain]), LandAny, [Elements.Fire, Elements.Air, Elements.Earth], "Joshua Wright", "2 Damage. Destroy all Explorer. If target land is Jungle / Wetland, add 1 Blight. -If you have- 2 Fire, 3 Air, 2 Earth: +4 Damage. Add 1 Wilds."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Savage Transformation", 2, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Moon, Elements.Animal], "Loic Belliau", "2 Fear. Replace 1 Explorer with 1 Beasts. -If you have- 2 Moon, 3 Animal: Replace 1 additional Explorer with 1 Beasts in either target or adjacent land."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Sea Monsters", 5, Speed.Slow, new Ranges(Source.Presence, 1), [Land.Coastal, Land.Wetland], [Elements.Water, Elements.Animal], "Moro Rogers", "Add 1 Beasts. If Invaders are present, 2 Fear per Beasts (max. 8 Fear). 3 Damage per Beasts. 1 Damage per Blight. -If you have- 3 Water, 3 Animal: Repeat this power."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Tigers Hunting", 2, Speed.Fast, new Ranges(Source.Presence, 1, [Land.Jungle]), TargetProperty.NoBlight, [Elements.Sun, Elements.Moon, Elements.Animal], "Cari Corene", "2 Fear. Add 1 Beasts. Gather up to 1 Beasts. 1 Damage per Beasts. Push up to 2 Beasts. -If you have- 2 Sun, 2 Moon, 3 Animal: 1 Damage in an adjacent land without Blight, and +1 Damage per Beasts there."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Unrelenting Growth", 4, Speed.Slow, null, TargetSpirit.Any, [Elements.Sun, Elements.Fire, Elements.Water, Elements.Plant], "Joshua Wright", "Target Spirit adds 2 Presence and 1 Wilds to a land at 1 Range of their Presence. -If you have- 3 Sun, 3 Plant: In that land, add 1 additional Wilds and remove 1 Blight. Target Spirit gains a Power Card."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Volcanic Eruption", 8, Speed.Slow, new Ranges(Source.Presence, 1, [Land.Mountain]), LandAny, [Elements.Fire, Elements.Earth], "Nolan Nasser", "6 Fear. 20 Damage. Destroy all Dahan and Beasts. Add 1 Blight. -If you have- 4 Fire, 3 Earth: Destroy all Invaders. Add 1 Wilds. In each adjacent land: 10 Damage. Destroy all Dahan and Beasts. If there are no Blight, add 1 Blight."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Sweep into the Sea", 4, Speed.Slow, new Ranges(Source.Presence, 2), LandAny, [Elements.Sun, Elements.Air, Elements.Water], "Joshua Wright", "Push all Explorer and Town one land towards the nearest Ocean. -or- If target land is Coastal, destroy all Explorer and Town. -If you have- 3 Sun, 2 Water: Repeat on an adjacent land."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Manifest Incarnation", 6, Speed.Slow, new Ranges(Source.Presence, 0), TargetProperty.City, [Elements.Sun, Elements.Moon, Elements.Earth, Elements.Animal], "Moro Rogers", "6 Fear. +1 Fear for each Town / City and for each of your Presence in target land. Remove 1 City, 1 Town and 1 Explorer. Then Invaders in target land Ravage. -If you have- 3 Sun, 3 Moon: +3 Fear. Invaders do -6 Damage on their Ravage."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Smothering Infestation", 3, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Water, Elements.Plant], "Joshua Wright", "Add 1 Disease. If target land is Jungle / Wetland, 2 Fear and 3 Damage. -If you have- 2 Water, 2 Plant: 1 Damage to each Invader."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Twisted Flowers Murmur Ultimatums", 5, Speed.Slow, new Ranges(Source.SacredSite, 1), TargetProperty.Invaders, [Elements.Sun, Elements.Moon, Elements.Air, Elements.Earth, Elements.Plant], "Kat Birmelin", "4 Fear. Add 1 Strife. If the Terror Level is 2 or higher, remove 2 Invaders. -If you have- 3 Moon, 2 Air, 3 Plant: +3 Fear, before the Terror Level check. 3 Damage."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Major, "Unlock the Gates of Deepest Power", 4, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Moon, Elements.Fire, Elements.Air, Elements.Water, Elements.Earth, Elements.Plant, Elements.Animal], "Joshua Wright", "Target Spirit gains a Major Power by drawing 2 and keeping 1, without having to Forget another Power Card. -If you have- 2 Sun, 2 Moon, 2 Fire, 2 Air, 2 Water, 2 Earth, 2 Plant, 2 Animal: Target Spirit may now play the Major Power they keep by paying half its cost (round up) OR by Forgetting it at the end of turn. It gains all elemental thresholds."),
        // Minor
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Inflame the Fires of Life", 1, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Moon, Elements.Fire, Elements.Plant, Elements.Animal], "Kat Birmelin", "Add 1 Disease. -or- 1 Fear. Add 1 Strife. -If you have- 3 Animal: You may do both."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Fire in the Sky", 1, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Sun, Elements.Fire, Elements.Air], "Moro Rogers", "2 Fear. Add 1 Strife"),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Fleshrot Fever", 1, Speed.Slow, new Ranges(Source.Presence, 1), [Land.Jungle, Land.Sands], [Elements.Fire, Elements.Air, Elements.Water, Elements.Animal], "Joshua Wright", "1 Fear. Add 1 Disease."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Gold's Allure", 0, Speed.Slow, new Ranges(Source.Presence, 1), [Land.Mountain], [Elements.Fire, Elements.Earth, Elements.Animal], "Lucas Durham", "Gather 1 Explorer. and 1 Town. Add 1 Strife."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Guardian Serpents", 1, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Moon, Elements.Earth, Elements.Animal], "Moro Rogers", "Add 1 Beasts in one of target Spirit's lands. If target Spirit has a SacredSite in that land: Defend 4 there."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Here there be Monsters", 0, Speed.Slow, new Ranges(Source.Presence, 0), Land.Inland, [Elements.Moon, Elements.Air, Elements.Animal], "Joshua Wright", "You may Push 1 Explorer / Town / Dahan. 2 Fear. If target land has any Beasts, 1 Fear."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Infested Aquifers", 1, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Moon, Elements.Water, Elements.Earth, Elements.Animal], "Nolan Nasser", "If target land has any Disease, 1 Damage to each Invader. -or- If target land is Mountain / Wetland, 1 Fear and add 1 Disease."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Poisoned Dew", 1, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Fire, Elements.Water, Elements.Plant], "Cari Corene", "Destroy 1 Explorer. If target land is Jungle / Wetland, destroy all Explorer."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Portents of Disaster", 0, Speed.Fast, new Ranges(Source.SacredSite, 1), TargetProperty.Invaders, [Elements.Sun, Elements.Moon, Elements.Air], "Nolan Nasser", "2 Fear. The next time an Invader is destroyed in target land this turn, 1 Fear."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Prowling Panthers", 1, Speed.Slow, new Ranges(Source.Presence, 1), [Land.Mountain, Land.Jungle], [Elements.Moon, Elements.Fire, Elements.Animal], "Moro Rogers", "1 Fear. Add 1 Beasts. -or- If target land has Beasts, destroy 1 Explorer / Town."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Renewing Rain", 1, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Water, Elements.Earth, Elements.Plant], "Nolan Nasser", "If target land is Jungle / Sands, remove 1 Blight. -If you have- 3 Plant: Add 1 Wilds."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Rites of the Land's Rejection", 1, Speed.Fast, new Ranges(Source.SacredSite, 2), TargetProperty.Dahan, [Elements.Moon, Elements.Fire, Elements.Earth], "Joshua Wright", "Invaders do not Build in target land this turn. 1 Fear per Town / City or 1 Fear per Dahan, whichever is less. -or- Push up to 3 Dahan."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Pact of the Joined Hunt", 1, Speed.Slow, null, TargetSpirit.Any, [Elements.Sun, Elements.Plant, Elements.Animal], "Jorge Ramos", "Target Spirit Gathers 1 Dahan into one of their lands. 1 Damage in that land per Dahan present."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Razor-Sharp Undergrowth", 1, Speed.Fast, new Ranges(Source.Presence, 0), TargetProperty.NoBlight, [Elements.Moon, Elements.Plant], "Cari Corene", "Destroy 1 Explorer and 1 Dahan. Add 1 Wilds. Defend 2."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Growth through Sacrifice", 0, Speed.Fast, null, TargetSpirit.Any, [Elements.Moon, Elements.Fire, Elements.Water, Elements.Plant], "Lucas Durham", "Destroy 1 of your Presence. Target Spirit chooses to either: Remove 1 Blight from one of their lands. -or- Add 1 Presence to one of their lands. -If you have- 2 Sun: They may do both, in the same land."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Scour the Land", 1, Speed.Slow, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Air, Elements.Earth], "Joshua Wright", "Destroy 3 Town and all Explorer. Add 1 Blight. -If you have- 3 Air: This power may be Fast."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Sky Stretches to Shore", 1, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Air, Elements.Water, Elements.Earth], "Joshua Wright", "This turn, target Spirit may use 1 Slow Power as if it were Fast, or vice versa. Target Spirit gains +3 Range for measuring Range to Coastal lands."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Swarming Wasps", 0, Speed.Fast, new Ranges(Source.Presence, 1), TargetProperty.NoBlight, [Elements.Fire, Elements.Air, Elements.Animal], "Joshua Wright", "Add 1 Beasts. -or- If target land has Beasts, Push up to 2 Explorer."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Absorb Corruption", 1, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Sun, Elements.Earth, Elements.Plant], "Nolan Nasser", "Gather 1 Blight. -or- Pay 1 Energy to remove 1 Blight. -If you have- 2 Plant: You may do both."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Animated Wrackroot", 0, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Moon, Elements.Fire, Elements.Plant], "Joshua Wright", "1 Fear. Destroy 1 Explorer. -or- Add 1 Wilds."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Promises of Protection", 0, Speed.Fast, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Sun, Elements.Earth, Elements.Animal], "Lucas Durham", "Gather up to 2 Dahan. Dahan have +2 Health while in target land."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Call to Ferocity", 0, Speed.Slow, new Ranges(Source.Presence, 1), TargetProperty.Invaders, [Elements.Sun, Elements.Fire, Elements.Earth], "Joshua Wright", "Gather up to 3 Dahan. -or- If target land has Dahan, 1 Fear and Push 1 Explorer and 1 Town."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Call to Trade", 1, Speed.Fast, new Ranges(Source.Presence, 2), TargetProperty.Dahan, [Elements.Air, Elements.Water, Elements.Earth, Elements.Plant], "Kat Birmelin", "You may Gather 1 Dahan. If the Terror Level is 2 or lower, Gather 1 Town and the first Ravage in target land this turn becomes a Build there instead."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Confounding Mists", 1, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Air, Elements.Water], "Loic Belliau", "Defend 4. -or- Each Invader added to target land this turn may be immediately Pushed to any adjacent land."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Cycles of Time and Tide", 1, Speed.Fast, new Ranges(Source.Presence, 1), [Land.Coastal], [Elements.Sun, Elements.Moon, Elements.Water], "Joshua Wright", "If there are Dahan, add 1 Dahan. If there are no Dahan, remove 1 Blight."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Disorienting Landscape", 1, Speed.Fast, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Moon, Elements.Air, Elements.Plant], "Nolan Nasser", "Push 1 Explorer. If target land is Mountain / Jungle, add 1 Wilds."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Elusive Ambushes", 1, Speed.Fast, new Ranges(Source.Presence, 1), TargetProperty.Dahan, [Elements.Sun, Elements.Fire, Elements.Water], "Nolan Nasser", "1 Damage. -or- Defend 4."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Tormenting Rotflies", 1, Speed.Slow, new Ranges(Source.Presence, 2), [Land.Sands, Land.Wetland], [Elements.Air, Elements.Plant, Elements.Animal], "Kat Birmelin", "Add 1 Disease. -or- If target land has Invaders, 2 Fear. If Disease is present, +1 Fear. If Blight is present, +1 Fear."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Twilight Fog brings Madness", 0, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Moon, Elements.Air, Elements.Water], "Loic Belliau", "Add 1 Strife. Push 1 Dahan. Each remaining Dahan takes 1 Damage."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Teeming Rivers", 1, Speed.Slow, new Ranges(Source.SacredSite, 2), [Land.Mountain, Land.Wetland], [Elements.Sun, Elements.Water, Elements.Plant, Elements.Animal], "Lucas Durham", "If target land has no Blight, add 1 Beasts. If target land has exactly 1 Blight, remove it."),
        new PowerCard(ProductSet.BranchAndClaw, PowerDeckType.Minor, "Spur on with Words of Fire", 1, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Fire, Elements.Air], "Nolan Nasser", "If you target a Spirit other than yourself, they gain +1 Energy. Target Spirit may immediately play another Power Card by paying its cost. (If it is Slow, it does not resolve until later.)"),
        // Uniques
        new PowerCard(ProductSet.BranchAndClaw, Unique.SharpFangsBehindTheLeaves, "Prey on the Builders", 1, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Moon, Elements.Fire, Elements.Animal], "Moro Rogers", "You may Gather 1 Beasts. If target land has Beasts, Invaders do not Build there this turn."),
        new PowerCard(ProductSet.BranchAndClaw, Unique.SharpFangsBehindTheLeaves, "Teeth Gleam from Darkness", 1, Speed.Slow, new Ranges(Source.Presence, 1, [Land.Jungle]), TargetProperty.NoBlight, [Elements.Moon, Elements.Plant, Elements.Animal], "Moro Rogers", "1 Fear. Add 1 Beasts. -or- If target land has both Beasts and Invaders: 3 Fear."),
        new PowerCard(ProductSet.BranchAndClaw, Unique.SharpFangsBehindTheLeaves, "Too Near the Jungle", 0, Speed.Slow, new Ranges(Source.Presence, 1, [Land.Jungle]), LandAny, [Elements.Plant, Elements.Animal], "Moro Rogers", "1 Fear. Destroy 1 Explorer."),
        new PowerCard(ProductSet.BranchAndClaw, Unique.SharpFangsBehindTheLeaves, "Terrifying Chase", 1, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Sun, Elements.Animal], "Moro Rogers", "Push 2 Explorer / Town / Dahan. Push another 2 Explorer / Town / Dahan per Beasts in target land. If you Pushed any Invaders, 2 Fear."),
        new PowerCard(ProductSet.BranchAndClaw, Unique.KeeperOfTheForbiddenWilds, "Towering Wrath", 3, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Sun, Elements.Fire, Elements.Plant], "Joshua Wright", "2 Fear. For each of your SacredSite in / adjacent to target land, 2 Damage. Destroy all Dahan."),
        new PowerCard(ProductSet.BranchAndClaw, Unique.KeeperOfTheForbiddenWilds, "Regrow from Roots", 1, Speed.Slow, new Ranges(Source.Presence, 1), [Land.Jungle, Land.Wetland], [Elements.Water, Elements.Earth, Elements.Plant], "Joshua Wright", "If there are 2 Blight or fewer in target land, remove 1 Blight."),
        new PowerCard(ProductSet.BranchAndClaw, Unique.KeeperOfTheForbiddenWilds, "Boon of Growing Power", 1, Speed.Slow, null, TargetSpirit.Any, [Elements.Sun, Elements.Moon, Elements.Plant], "Joshua Wright", "Target Spirit gains a Power Card. If you target another Spirit, they also gain 1 Energy."),
        new PowerCard(ProductSet.BranchAndClaw, Unique.KeeperOfTheForbiddenWilds, "Sacrosanct Wilderness", 2, Speed.Fast, new Ranges(Source.Presence, 1), TargetProperty.NoBlight, [Elements.Sun, Elements.Earth, Elements.Plant], "Joshua Wright", "Push 2 Dahan. 2 Damage per Wilds in target land. -or- Add 1 Wilds."),
        // Promo
        // Uniques
        new PowerCard(ProductSet.Promo, Unique.HeartOfTheWildfire, "Flash-Fires", 2, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Fire, Elements.Air], "Nolan Nasser", "1 Fear. 1 Damage. -If you have- 2 Air: This Power is Fast."),
        new PowerCard(ProductSet.Promo, Unique.HeartOfTheWildfire, "Asphyxiating Smoke", 2, Speed.Slow, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Fire, Elements.Air, Elements.Plant], "Nolan Nasser", "1 Fear. Destroy 1 Town. Push 1 Dahan."),
        new PowerCard(ProductSet.Promo, Unique.HeartOfTheWildfire, "Flame's Fury", 0, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Fire, Elements.Plant], "Nolan Nasser", "Target Spirit gains 1 Energy. Target Spirit does +1 Damage with each Damage dealing Power they use this turn. (Powers which damage multiple lands or each Invader only get 1 extra damage total. Repeated Powers keep the +1 boost. Destroy effects don't get any bonus.)"),
        new PowerCard(ProductSet.Promo, Unique.HeartOfTheWildfire, "Threatening Flames", 0, Speed.Fast, new Ranges(Source.Presence, 0), [TargetProperty.Blight, TargetProperty.Invaders], [Elements.Fire, Elements.Plant], "Nolan Nasser", "2 Fear. Push 1 Explorer / Town per Terror Level from target land to adjacent lands without your Presence. If there are no such adjacent lands, +2 Fear."),
        new PowerCard(ProductSet.Promo, Unique.SerpentSlumberingBeneathTheIsland, "Gift of the Primordial Deeps", 1, Speed.Fast, null, TargetSpirit.Another, [Elements.Moon, Elements.Earth], "Jorge Ramos", "Target Spirit gains a Minor Power. Target Spirit chooses to either: Play it immediately by paying its cost. -or- Gain 1 Moon and 1 Earth."),
        new PowerCard(ProductSet.Promo, Unique.SerpentSlumberingBeneathTheIsland, "Gift of Flowing Power", 1, Speed.Fast, null, TargetSpirit.Another, [Elements.Fire, Elements.Water], "Jorge Ramos", "Target Spirit gains 1 Energy. Target Spirit chooses to either: Play another Power Card by paying its cost. -or- Gain 1 Fire and 1 Water."),
        new PowerCard(ProductSet.Promo, Unique.SerpentSlumberingBeneathTheIsland, "Absorb Essence", 2, Speed.Fast, null, TargetSpirit.Another, [Elements.Moon, Elements.Fire, Elements.Water, Elements.Earth], "Jorge Ramos", "Gain 3 Energy. Move 1 of target Spirit's Presence from the board to your \"Deep Slumber\" track. Absorbed Presence cannot be returned to play. Target Spirit gains 1 Any and 1 Energy."),
        new PowerCard(ProductSet.Promo, Unique.SerpentSlumberingBeneathTheIsland, "Elemental Aegis", 1, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Fire, Elements.Water, Elements.Earth], "Jorge Ramos", "Defend 2 in target land and all adjacent lands. For every Presence on your \"Deep Slumber\" track, Defend 1 in target land and all adjacent lands."),
        // Jagged Earth
        // Major
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Forests of Living Obsidian", 4, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Sun, Elements.Fire, Elements.Earth, Elements.Plant], "Lucas Durham", "Add 1 Badlands. Push all Dahan. 1 Damage to each Invader. If the origin land is your Sacred Site, +1 Damage to each Invader.  -If you have- 2 Sun, 3 Fire, 3 Earth: Repeat this Power."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Infestation of Venomous Spiders", 4, Speed.Fast, new Ranges(Source.SacredSite, 2), TargetProperty.Invaders, [Elements.Air, Elements.Earth, Elements.Plant, Elements.Animal], "Lucas Durham", "Add 1 Beasts. Gather up to 1 Beasts. For each Beasts, 1 Fear (max. 4) and Invaders skip one Action in target land. -If you have- 2 Air, 2 Earth, 3 Animal: After this Power causes Invaders to skip an Action, 4 Damage."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Dream of the Untouched Land", 6, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Moon, Elements.Water, Elements.Earth, Elements.Plant, Elements.Animal], "Joshua Wright", "Remove up to 3 Blight and up to 3 Health worth of Invaders.  -If you have- 3 Moon, 2 Water, 3 Earth, 2 Plant: (Max. 1x/game) Add a random new Island Board next to target board. Ignore its Setup icons; add 2 Beasts, 2 Wilds, 2 Badlands and up to 2 Presence (from any Spirits) anywhere on it. From now on, Build cards and \"Each board / Each land\" Adversary Actions skip 1 Board."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Angry Bears", 3, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Sun, Elements.Fire, Elements.Animal], "Moro Rogers", "2 Fear. 2 Damage. If no Beasts are present, add 1 Beasts. Otherwise, +2 Damage, and Push up to 1 Beasts.  -If you have- 2 Fire, 3 Animal: 1 Fear and destroy 1 Explorer / Town in an adjacent land with Beasts."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Focus the Land's Anguish", 5, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun], "Moro Rogers", "If this Power Destroys any Town / City, 5 Fear. Gather up to 5 Blight. 1 Damage per Blight.  -If you have- 3 Sun: +1 Damage per Blight."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Vanish Softly Away, Forgotten by All", 3, Speed.Slow, new Ranges(Source.Presence, 2), LandAny, [Elements.Moon, Elements.Air], "Joshua Wright", "Remove 1 Invader and 1 Explorer / Town. -or- Remove all Damaged Invaders. Adversary or Scenario rules that prevent or alter Removal do not affect this Power.  -If you have- 3 Moon, 3 Air: In any 2 lands with 4 or more Invaders: Remove 1 Invader."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Unleash a Torrent of the Self's Own Essence", 2, Speed.Fast, null, TargetSpirit.Yourself, [Elements.Sun, Elements.Moon, Elements.Fire, Elements.Water], "Moro Rogers", "Gain 4 energy. You may forget a power card to gain 4 more energy. -or- Pay X energy (min. 1) to deal X damage in a land at 0 Range.  -If you have- 2 Sun, 3 Fire: You may do both."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Bargains of Power and Protection", 2, Speed.Fast, new Ranges(Source.Presence, 0), TargetProperty.Dahan, [Elements.Sun, Elements.Water, Elements.Earth, Elements.Animal], "Joshua Wright", "Remove 1 of your Presence on the island from the game, setting it on the Reminder Card. From now on: each Dahan within 1 Range of your Presence provides Defend 1 in its land, and you gain 1 less Energy each turn. (This effect stacks if used multiple times) -If you have- 3 Sun, 2 Water, 2 Earth: The Presence instead comes from your Presence track."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Transform to a Murderous Darkness", 6, Speed.Slow, null, TargetSpirit.Any, [Elements.Moon, Elements.Fire, Elements.Air, Elements.Water, Elements.Plant], "Moro Rogers", "Target Spirit may choose one of their Sacred Sites. In that land: Replace all their Presence with Badlands; the replaced Presence leave the game. Push any number of those Badlands. 3 Fear. 3 Damage per Presence replaced. -If you have- 3 Moon, 2 Fire, 2 Air: 1 Damage in an adjacent land. 1 Damage in an adjacent land."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Settle Into Hunting-Grounds", 3, Speed.Fast, null, TargetSpirit.Yourself, [Elements.Moon, Elements.Fire, Elements.Plant, Elements.Animal], "Moro Rogers", "Your Presence may count as Badlands and Beasts. (Decide per Presence, per action.) Your Presence cannot move. -If you have- 2 Plant, 3 Animal: 2 Fear and 2 Damage in one of your lands."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Walls of Rock and Thorn", 4, Speed.Fast, new Ranges(Source.SacredSite, 2), [Land.Mountain, Land.Jungle], [Elements.Sun, Elements.Earth, Elements.Plant], "Joshua Wright", "2 Damage. Defend 8. Add 1 Wilds. Isolate target land. -If you have- 2 Earth, 2 Plant: +2 Damage. +2 Defend. Add 1 Badlands."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Voice of Command", 3, Speed.Fast, new Ranges(Source.SacredSite, 1), TargetProperty.Dahan, [Elements.Sun, Elements.Air], "Lucas Durham", "1 Damage per Dahan / Explorer, to Town / City only. Defend 2. During Ravage actions, Explorer fight alongside Dahan. (Deal / take damage at the same time, and to / from the same sources.) -If you have- 3 Sun, 2 Air: First, Gather up to 2 Explorer / Town / Dahan"),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Irresistible Call", 6, Speed.Fast, new Ranges(Source.SacredSite, 2), TargetProperty.Inland, [Elements.Sun, Elements.Air, Elements.Plant], "Lucas Durham", "Gather 5 Town, 5 Dahan, 5 Beasts, and 15 Explorer. -If you have- 2 Sun, 3 Air, 2 Plant: Invaders skip all Actions in target land. Isolate target land."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "The Wounded Wild Turns on its Assailants", 4, Speed.Slow, new Ranges(Source.Presence, 1), TargetProperty.Blight, [Elements.Fire, Elements.Plant, Elements.Animal], "Joshua Wright", "Add 2 Badlands. Gather up to 2 Beasts. 1 Damage per Blight / Beasts / Wilds. -If you have- 2 Fire, 3 Plant, 2 Animal: 2 Fear per Invader destroyed by the Power (max. 8 Fear)."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Draw Towards a Consuming Void", 8, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [], "Joshua Wright", "Gather 1 Explorer, 1 Town, 1 City, 1 Dahan, 1 Beasts, and 1 Presence (from any Spirit) from each adjacent land. 4 Fear. 15 Damage. 5 Damage to Dahan. Destroy 1 Presence from each Spirit. Destroy 2 Beasts. -If you have no other power cards in play-: Any number of times: Forget a Minor Power, and Major Power, and a Unique Power to perform the above effects again."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Storm-Swath", 3, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Fire, Elements.Air, Elements.Water], "Jorge Ramos", "2 Fear. In both origin land and target land: 1 Damage to each Invader. -If you have- 2 Fire, 3 Air, 2 Water: +1 Fear. This Power has +1 Range. In a land adjacent to both origin and target, 1 Damage to each Invader. In lands where you did Damage, destroy 1 town."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Spill Bitterness into the Earth", 5, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Fire, Elements.Water, Elements.Earth], "Moro Rogers", "6 Damage. Add 2 Badlands / Strife and 1 Blight. In up to 3 adjacent lands with Blight, add 1 Badlands / Strife. -If you have- 3 Fire, 3 Water: In up to 3 adjacent lands, 1 Damage to each Invader."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Utter a Curse of Dread and Bone", 4, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Moon, Elements.Animal], "Joshua Wright", "For each Blight in / adjacent to target land, add 1 Badlands, 1 Disease, or 1 Strife. (Max. +3 of each.) Then: 2 Fear. 1 Damage. -If you have- 3 Moon, 2 Animal: For each type of token you added, add 1 more within 1 Range. 1 Damage in an adjacent land."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Sleep and Never Waken", 3, Speed.Fast, new Ranges(Source.Presence, 2, [Land.Sands]), LandAny, [Elements.Moon, Elements.Air, Elements.Earth, Elements.Animal], "Joshua Wright", "Invaders skip all Actions in target land. 1 Fear per 2 Explorer this Power removes. Remove up to 2 Explorer. -If you have- 3 Moon, 2 Air, 2 Animal: Remove up to 6 Explorer from among your lands."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Weave Together the Fabric of Place", 4, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Sun, Elements.Moon, Elements.Air, Elements.Water, Elements.Earth], "Joshua Wright", "Target land and a land adjacent to it become a single land for this turn. (It has the terrain and land # of both lands. When this effect expires, divide pieces as you wish; all of them are considered moved.) -If you have- 4 Air: Isolate the joined land. If it has Invaders, 2 Fear, and remove up to 2 Invaders."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Trees Radiate Celestial Brilliance", 3, Speed.Fast, new Ranges(Source.Presence, 1), [Land.Jungle, TargetProperty.NoBlight], [Elements.Sun, Elements.Moon, Elements.Plant], "Shawn Daley", "3 Fear. Defend 6. Invaders skip the next build. (In target land this turn.) -If you have- 3 Sun, 2 Moon, 2 Plant: 1 Damage per Sun you have."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Thickets Erupt with Every Touch of Breeze", 3, Speed.Fast, new Ranges(Source.SacredSite, 2), TargetProperty.Inland, [Elements.Air, Elements.Plant], "Jorge Ramos", "2 Damage. Then either: Add 3 Wilds. -or- Remove 1 Blight. -If you have- 3 Plant: 1 Fear. +2 Damage."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Major, "Melt Earth into Quicksand", 4, Speed.Fast, new Ranges(Source.Presence, 1), [Land.Sands, Land.Wetland], [Elements.Moon, Elements.Water, Elements.Earth], "Lucas Durham", "1 Fear. 2 Damage. Isolate target land. After Invaders / Dahan are Moved into target land, Destroy them.  -If you have- 2 Moon, 4 Water, 2 Earth: +4 Damage. Add 1 Badlands. Add 1 Wilds."),
        // Minor
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Hazards Spread Across The Island", 0, Speed.Fast, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Fire, Elements.Air, Elements.Earth, Elements.Plant], "Kat Guevara", "Choose a type of token from Badlands / Beasts / Disease / Strife / Wilds that exists in an adjacent land; choosing Disease costs 1 energy. Add 1 of that type of token to target land."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Bats Scout For Raids By Darkness", 1, Speed.Slow, new Ranges(Source.Presence, 2), LandAny, [Elements.Moon, Elements.Air, Elements.Animal], "Shawn Daley", "For each Dahan, 1 Damage to Town / City. -or- 1 Fear. Gather up to 2 Dahan."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Birds Cry Warning", 1, Speed.Fast, new Ranges(Source.Presence, 3), TargetProperty.Dahan, [Elements.Sun, Elements.Air, Elements.Animal], "Joshua Wright", "The next time Dahan would be Destroyed in target land, Destroy 2 fewer Dahan. -or- Push up to 3 Dahan."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Blood Draws Predators", 1, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Fire, Elements.Water, Elements.Animal], "Kat Guevara", "After the next time Invaders are Destroyed in target land: Add 1 Beasts, then 1 Damage per Beasts (max. 3 Damage)."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Carapaced Land", 0, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Earth, Elements.Plant, Elements.Animal], "Kat Guevara", "If targeting a land with Beasts, this Power has +1 Range. Defend 3. -If you have- 2 Earth: Defend +3."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Call To Guard", 0, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Air, Elements.Earth], "Kat Guevara", "Gather up to 1 Dahan. Then, if Dahan are present, either: Defend 1 per Dahan. -or- After Invaders are added or moved to target land, 1 Damage to each added or moved Invader."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Desiccating Winds", 1, Speed.Slow, new Ranges(Source.SacredSite, 1), [Land.Mountain, Land.Sands], [Elements.Fire, Elements.Air, Elements.Earth], "Shawn Daley", "If target land has Badlands, 1 Damage. Add 1 Badlands."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Dry Wood Explodes In Smoldering Splinters", 1, Speed.Slow, new Ranges(Source.Presence, 0), TargetProperty.NoWetland, [Elements.Fire, Elements.Air, Elements.Plant], "Jorge Ramos", "You may spend 1 Energy to make this Power Fast. 2 Fear. 1 Damage."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Gift of Nature's Connection", 0, Speed.Fast, null, TargetSpirit.Any, [], "Moro Rogers", "Target Spirit gains either 2 Energy or 2 of a single Element (their choice). If you target another Spirit, you gain an Element of your choice."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Entrap The Forces Of Corruption", 1, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Earth, Elements.Plant, Elements.Animal], "Shawn Daley", "Gather up to 1 Blight. Isolate target land. When Blight is added to target land, it doesn't cascade."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Domesticated Animals Go Berserk", 1, Speed.Fast, new Ranges(Source.Presence, 0), [TargetProperty.Town, TargetProperty.City], [Elements.Moon, Elements.Fire, Elements.Animal], "Joshua Wright", "1 Fear. Defend 5. -If you have- 3 Moon: Add 1 Beasts."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Dire Metamorphosis", 1, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Moon, Elements.Air, Elements.Earth, Elements.Animal], "Moro Rogers", "1 Fear. 1 Damage. 1 Damage to Dahan. Add 1 Badlands, 1 Beasts, 1 Disease, 1 Strife, 1 Wilds, and 1 Blight."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Skies Herald The Season Of Return", 1, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Moon, Elements.Plant, Elements.Animal], "Joshua Wright", "A Spirit with Presence on target board may add 1 of their Destroyed Presence. Gather up to 2 Dahan. Push 1 Blight."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Gift of Twinned Days", 1, Speed.Fast, null, TargetSpirit.Another, [Elements.Sun, Elements.Moon], "Joshua Wright", "Once this turn, target Spirit may Repeat the lowest-cost Power Card they have in play by paying it's cost again. You may do likewise."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Haunted By Primal Memories", 1, Speed.Fast, new Ranges(Source.SacredSite, 2), TargetProperty.Invaders, [Elements.Moon, Elements.Air, Elements.Earth], "Kat Guevara", "1 Fear. Defend 3. If Beasts are present, +2 Fear."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Like Calls to Like", 1, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Water, Elements.Plant], "Kat Guevara", "If target land has Explorer, Gather up to 1 Explorer. Do likewise for Town, Dahan, Blight, and Beasts."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Unquenchable Flames", 1, Speed.Slow, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Moon, Elements.Fire, Elements.Earth], "Kat Guevara", "1 Fear. 1 Damage to Town / City. Invaders do not heal Damage at end of turn. -If you have- 2 Fire: Add 1 Badlands."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Mesmerized Tranquility", 0, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Water, Elements.Earth, Elements.Animal], "Kat Guevara", "Isolate target land. Each Invader does -1 Damage."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Territorial Strife", 0, Speed.Slow, new Ranges(Source.Presence, 1), TargetProperty.City, [Elements.Sun, Elements.Fire, Elements.Animal], "Kat Guevara", "3 Damage to Explorer / Town. -or- Add 1 Strife."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Renewing Boon", 1, Speed.Slow, null, TargetSpirit.Another, [Elements.Sun, Elements.Earth, Elements.Plant], "Joshua Wright", "Choose a land where you and target Spirit both have Presence. In that land: Remove 1 Blight, and target Spirit may add 1 of their Destroyed Presence."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Scream Disease Into The Wind", 1, Speed.Fast, null, TargetSpirit.Another, [Elements.Air, Elements.Water, Elements.Animal], "Moro Rogers", "Target Spirit gets +1 Range with all their Powers. Once this turn, after target Spirit uses a Power targeting a land, they may add 1 Disease to that land. (Hand them a Disease token as a reminder.)"),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Sear Anger Into The Wild Lands", 0, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Fire, Elements.Plant], "Kat Guevara", "Add 1 Badlands. -or- If Wilds and Invaders are present, 1 Fear and 1 Damage."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Set Them On An Ever-Twisting Trail", 1, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Air, Elements.Plant, Elements.Animal], "Joshua Wright", "Gather or Push 1 Explorer. Isolate target land."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Strong And Constant Currents", 0, Speed.Fast, new Ranges(Source.Presence, 0), Land.Coastal, [Elements.Sun, Elements.Water, Elements.Earth], "Jorge Ramos", "Push 1 Explorer / Town to an adjacent Coastal land. -or- Move up to 2 Dahan between target land and one other Coastal land. -If you have- 2 Water: You may do both."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Sucking Ooze", 0, Speed.Fast, new Ranges(Source.Presence, 1), [Land.Sands, Land.Wetland], [Elements.Moon, Elements.Water, Elements.Earth], "Moro Rogers", "2 Fear if Invaders are present. Isolate target land."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Sunset's Fire Flows Across The Land", 1, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Sun, Elements.Moon, Elements.Fire, Elements.Water], "Moro Rogers", "1 Fear. 1 Damage. You may pay 1 Energy to deal 1 Damage in an adjacent land."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Terror Turns To Madness", 0, Speed.Slow, new Ranges(Source.Presence, 2), TargetProperty.Invaders, [Elements.Moon, Elements.Air, Elements.Water], "Shawn Daley", "If the Terror Level is... Terror Level 1: 3 Fear. Terror Level 2: 2 Fear or add 1 Strife. Terror Level 3: Add 1 Strife."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "The Shore Seethes With Hatred", 1, Speed.Slow, new Ranges(Source.Presence, 1), Land.Coastal, [Elements.Fire, Elements.Water, Elements.Earth, Elements.Plant], "Joshua Wright", "1  Fear. Add 1 Badlands and 1 Wilds."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Thriving Chokefungus", 1, Speed.Slow, new Ranges(Source.SacredSite, 1), [Land.Jungle, Land.Wetland], [Elements.Moon, Elements.Water, Elements.Plant], "Jorge Ramos", "Add 1 Disease and 1 Badlands."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Treacherous Waterways", 0, Speed.Fast, new Ranges(Source.Presence, 1), [Land.Mountain, Land.Wetland], [Elements.Fire, Elements.Water, Elements.Earth], "Kat Guevara", "Add 1 Wilds. -or- Push 1 Explorer."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Flow Downriver, Blow Downwind", 0, Speed.Slow, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Air, Elements.Water, Elements.Plant], "Joshua Wright", "Push up to 1 Blight / Explorer / Town."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Weep For What Is Lost", 0, Speed.Slow, new Ranges(Source.Presence, 1), TargetProperty.Blight, [Elements.Fire, Elements.Water, Elements.Animal], "Kat Guevara", "1 Fear per type of Invader present. Push up to 1 Explorer / Town per Blight."),
        new PowerCard(ProductSet.JaggedEarth, PowerDeckType.Minor, "Favor Of The Sun And Star-Lit Dark", 1, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Sun, Elements.Moon, Elements.Plant], "Moro Rogers", "Defend 4. Push up to 1 Blight. -If you have- 2 Sun: 1 Fear"),
        // Uniques
        new PowerCard(ProductSet.JaggedEarth, Unique.GrinningTricksterStirsUpTrouble, "Unexpected Tigers", 0, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Moon, Elements.Fire, Elements.Animal], "Joshua Wright", "1 Fear if Invaders are present. If you can gather 1 Beasts, do so, then push 1 Explorer. Otherwise, add 1 Beasts."),
        new PowerCard(ProductSet.JaggedEarth, Unique.GrinningTricksterStirsUpTrouble, "Impersonate Authority", 0, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Air, Elements.Animal], "Joshua Wright", "Add 1 Strife."),
        new PowerCard(ProductSet.JaggedEarth, Unique.GrinningTricksterStirsUpTrouble, "Incite the Mob", 1, Speed.Slow, new Ranges(Source.Presence, 1), TargetProperty.Invaders, [Elements.Moon, Elements.Fire, Elements.Air, Elements.Animal], "Joshua Wright", "1 Invader with Strife deals Damage to other Invaders (not to each Invader). 1 Fear per Invader this Power Destroyed."),
        new PowerCard(ProductSet.JaggedEarth, Unique.GrinningTricksterStirsUpTrouble, "Overenthusiastic Arson", 1, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Fire, Elements.Air], "Joshua Wright", "Destroy 1 Town. Discard the top card of the Minor Power Deck. If it provides Fire: 1 Fear, 2 Damage, and add 1 Blight."),
        new PowerCard(ProductSet.JaggedEarth, Unique.VolcanoLoomingHigh, "Rain of Ash", 2, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Fire, Elements.Air, Elements.Earth], "Moro Rogers", "2 Fear if Invaders are present. Push 2 Dahan and 2 Explorer / Town to land(s) without your Presence."),
        new PowerCard(ProductSet.JaggedEarth, Unique.VolcanoLoomingHigh, "Lava Flows", 1, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Fire, Elements.Earth], "Moro Rogers", "Add 1 Badlands and 1 Wilds. -or- 1 Damage."),
        new PowerCard(ProductSet.JaggedEarth, Unique.VolcanoLoomingHigh, "Exaltation of Molten Stone", 1, Speed.Fast, null, TargetSpirit.Another, [Elements.Moon, Elements.Fire, Elements.Earth], "Moro Rogers", "Split 1 Energy per Fire you have between yourself and target Spirit, as evenly as possible. Target Spirit gains +1 Range with their powers that originate from a Mountain."),
        new PowerCard(ProductSet.JaggedEarth, Unique.VolcanoLoomingHigh, "Pyroclastic Bombardment", 3, Speed.Fast, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Fire, Elements.Air, Elements.Earth], "Moro Rogers", "1 Damage to each Town / City / Dahan. 1 Damage. 1 Damage to Dahan."),
        new PowerCard(ProductSet.JaggedEarth, Unique.ShroudOfSilentMist, "Dissolving Vapors", 2, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Air, Elements.Water], "Emily Hancock", "1 Fear. 1 Damage to each Invader. 1 Damage to each Dahan."),
        new PowerCard(ProductSet.JaggedEarth, Unique.ShroudOfSilentMist, "The Fog Closes In", 1, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Moon, Elements.Air, Elements.Water], "Emily Hancock", "For each adjacent land with your Presence, 1 Damage to a different Invader. Push 2 Dahan."),
        new PowerCard(ProductSet.JaggedEarth, Unique.ShroudOfSilentMist, "Unnerving Pall", 1, Speed.Fast, new Ranges(Source.Presence, 0), TargetProperty.Invaders, [Elements.Moon, Elements.Air, Elements.Animal], "Emily Hancock", "1 Fear. Up to 3 damaged Invaders do not participate in Ravage. -or- 1 Fear. Defend 1 per Presence you have in target land (when this Power is used)."),
        new PowerCard(ProductSet.JaggedEarth, Unique.ShroudOfSilentMist, "Flowing and Silent Forms Dart By", 0, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Moon, Elements.Air, Elements.Water], "Emily Hancock", "2 Fear if Invaders are present. When Presence in target land would be Destroyed, its owner may, if possible, instead Push that Presence. You may Gather 1 Presence / Sacred Site of another Spirit (with their permission)."),
        new PowerCard(ProductSet.JaggedEarth, Unique.VengeanceAsABurningPlague, "Fiery Vengeance", 0, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Fire], "Damon Westenhofer", "Cost to Use: Target Spirit Removes 1 of their Destroyed Presence from the game. 1 Fear and 1 Damage in one of target Spirit's lands. (This is your Power, so Blight counts as Badlands, even if target is another Spirit.)"),
        new PowerCard(ProductSet.JaggedEarth, Unique.VengeanceAsABurningPlague, "Plaguebearers", 1, Speed.Slow, new Ranges(Source.Presence, 2), TargetProperty.Disease, [Elements.Fire, Elements.Water, Elements.Animal], "Damon Westenhofer", "1 Fear if Invaders are present. For each Disease, Push 2 Explorer / Town / Dahan. 1 Disease may move with each Pushed piece."),
        new PowerCard(ProductSet.JaggedEarth, Unique.VengeanceAsABurningPlague, "Fetid Breath Spreads Infection", 2, Speed.Slow, new Ranges(Source.Presence, 1), TargetProperty.Invaders, [Elements.Air, Elements.Water, Elements.Animal], "Damon Westenhofer", "1 Fear. Add 1 Disease."),
        new PowerCard(ProductSet.JaggedEarth, Unique.VengeanceAsABurningPlague, "Strike Low with Sudden Fevers", 2, Speed.Fast, new Ranges(Source.Presence, 1), TargetProperty.Disease, [Elements.Fire, Elements.Air, Elements.Earth, Elements.Animal], "Damon Westenhofer", "1 Fear. Invaders skip Ravage Actions."),
        new PowerCard(ProductSet.JaggedEarth, Unique.FracturedDaysSplitTheSky, "Absolute Stasis", 1, Speed.Fast, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Sun, Elements.Air, Elements.Earth], "Lucas Durham", "Cost to Use: 1 Time. Until the end of the Slow phase, target land and everything in it cease to exist for all purposes except checking victory/defeat. (You cannot target into, out of, or through where the land was.) This cannot target an Ocean even if Oceans are in play."),
        new PowerCard(ProductSet.JaggedEarth, Unique.FracturedDaysSplitTheSky, "Pour Time Sideways", 1, Speed.Fast, null, TargetSpirit.Yourself, [Elements.Moon, Elements.Air, Elements.Water], "Lucas Durham", "Cost to Use: 3 Time. Move 1 of your Presence to a different land with your Presence. On the board moved from: During the Invader Phase, Resolve Invader and \"Each board / Each land...\" Actions one fewer time. On the board moved to: During the Invader Phase, Resolve Invader and \"Each board / Each Land...\" Actions one more time."),
        new PowerCard(ProductSet.JaggedEarth, Unique.FracturedDaysSplitTheSky, "The Past Returns Again", 0, Speed.Fast, null, null, [Elements.Sun, Elements.Moon], "Lucas Durham", "Cost to Use: N Time, and Spirits jointly pay N Energy (where N = # of players). Swap the top card of the Invader Deck with a card in the Invader discard that is within 1 Invader Stage of it. (The discarded card stays face-down. You can't swap cards that don't exist.)"),
        new PowerCard(ProductSet.JaggedEarth, Unique.FracturedDaysSplitTheSky, "Blur the Arc of Years", 1, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Moon, Elements.Air], "Lucas Durham", "If no Dahan / Invaders are present: Remove 1 Blight. If invaders are present: they Build, then Ravage. If Dahan are present: Add 1 Dahan. Push up to 2 Dahan. You may repeat this power (once) on the same land by spending 1 Time."),
        new PowerCard(ProductSet.JaggedEarth, Unique.ShiftingMemoryOfAges, "Boon of Ancient Memories", 1, Speed.Slow, null, TargetSpirit.Any, [Elements.Moon, Elements.Water, Elements.Earth, Elements.Plant], "Joshua Wright", "If you target yourself, gain a Minor Power. Otherwise: Target Spirit gains a Power Card. If it's a Major Power, they may pay 2 Energy instead of Forgetting a Power Card."),
        new PowerCard(ProductSet.JaggedEarth, Unique.ShiftingMemoryOfAges, "Elemental Teachings", 0, Speed.Fast, null, TargetSpirit.Any, [Elements.Moon, Elements.Air, Elements.Earth], "Joshua Wright", "Prepare 1 Element Marker. Discard up to 3 Element Markers. Target Spirit gains those Elements. (They can be any combination of Elements - the same or different.)"),
        new PowerCard(ProductSet.JaggedEarth, Unique.ShiftingMemoryOfAges, "Share Secrets of Survival", 0, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Sun, Elements.Air, Elements.Earth], "Joshua Wright", "Each time Dahan would be Destroyed in target land, Destroy 2 fewer Dahan. -or- Gather up to 2 Dahan.  -If you have- 3 Air: You may do both."),
        new PowerCard(ProductSet.JaggedEarth, Unique.ShiftingMemoryOfAges, "Study the Invaders' Fears", 0, Speed.Fast, new Ranges(Source.Presence, 0), [TargetProperty.Town, TargetProperty.City], [Elements.Moon, Elements.Air, Elements.Animal], "Joshua Wright", "2 Fear. Turn the top card of the Fear Deck face-up."),
        new PowerCard(ProductSet.JaggedEarth, Unique.StarlightSeeksItsForm, "Boon of Reimagining", 1, Speed.Slow, null, TargetSpirit.Any, [Elements.Moon], "Emily Hancock", "Target Spirit may Forget a Power Card from hand or discard. If they do, they draw 6 Minor Power Cards and gain 2 of them. If you target another Spirit, they gain 1 Energy."),
        new PowerCard(ProductSet.JaggedEarth, Unique.StarlightSeeksItsForm, "Gather the Scattered Light of Stars", 0, Speed.Slow, null, TargetSpirit.Yourself, [Elements.Moon], "Emily Hancock", "At end of turn after discarding: Reclaim up to 2 cards to your hand. You may then Forget a Unique Power Card to Reclaim up to 3 additional cards."),
        new PowerCard(ProductSet.JaggedEarth, Unique.StarlightSeeksItsForm, "Shape the Self Anew", 0, Speed.Slow, null, TargetSpirit.Yourself, [Elements.Moon], "Emily Hancock", "Gain a Minor Power. You may Forget this Power Card to gain 3 Energy.  -If you have- 4 Moon: You may gain a Major Power instead of a Minor Power."),
        new PowerCard(ProductSet.JaggedEarth, Unique.StarlightSeeksItsForm, "Peace of the Nighttime Sky", 1, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Moon], "Emily Hancock", "If the Terror Level is 1, Invaders do not Ravage in target land this turn. You may Repeat this Power. If you do, Forget this Power Card and Gain 1 Moon."),
        new PowerCard(ProductSet.JaggedEarth, Unique.StonesUnyieldingDefiance, "Scarred and Stony Land", 2, Speed.Slow, new Ranges(Source.SacredSite, 1), TargetProperty.Blight, [Elements.Moon, Elements.Earth], "Moro Rogers", "2 Damage. Add 1 Badlands. Remove 1 Blight in target land from the game. (It goes to the box, not the Blight Card.)"),
        new PowerCard(ProductSet.JaggedEarth, Unique.StonesUnyieldingDefiance, "Plows Shatter on Rocky Ground", 2, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Earth], "Moro Rogers", "1 Damage to each Town / City. Push up to 1 Town. -or- Destroy 1 Town."),
        new PowerCard(ProductSet.JaggedEarth, Unique.StonesUnyieldingDefiance, "Jagged Shards Push from the Earth", 0, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Fire, Elements.Earth], "Moro Rogers", "Add 1 Badlands. Push up to 2 Dahan."),
        new PowerCard(ProductSet.JaggedEarth, Unique.StonesUnyieldingDefiance, "Stubborn Solidity", 1, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Earth, Elements.Animal], "Moro Rogers", "Defend 1 per Dahan. Dahan in target land cannot be changed. (When they would be Damaged, Destroyed, Removed, Replaced, or moved, instead don't)"),
        new PowerCard(ProductSet.JaggedEarth, Unique.LureOfTheDeepWilderness, "Perils of the Deepest Island", 1, Speed.Slow, new Ranges(Source.Presence, 0), TargetProperty.Inland, [Elements.Moon, Elements.Plant, Elements.Animal], "Joshua Wright", "1 Fear. Add 1 Badlands. Add 1 Beasts within 1 Range. Push up to 2 Dahan."),
        new PowerCard(ProductSet.JaggedEarth, Unique.LureOfTheDeepWilderness, "Softly Beckon Ever Inward", 2, Speed.Slow, new Ranges(Source.Presence, 0), TargetProperty.Inland, [Elements.Moon, Elements.Air], "Joshua Wright", "Gather up to 2 Explorer. Gather up to 2 Town. Gather up to 2 Beasts. Gather up to 2 Dahan."),
        new PowerCard(ProductSet.JaggedEarth, Unique.LureOfTheDeepWilderness, "Gift of the Untamed Wild", 0, Speed.Slow, null, TargetSpirit.Any, [Elements.Moon, Elements.Fire, Elements.Air, Elements.Plant], "Joshua Wright", "Target Spirit chooses to either: add 1 Wilds to one of their lands. -or- Replace 1 of their Presence with 1 Disease."),
        new PowerCard(ProductSet.JaggedEarth, Unique.LureOfTheDeepWilderness, "Swallowed by the Wilderness", 1, Speed.Fast, new Ranges(Source.Presence, 0), TargetProperty.Inland, [Elements.Fire, Elements.Air, Elements.Plant, Elements.Animal], "Joshua Wright", "2 Fear. 1 Damage per Beasts / Disease / Wilds / Badlands. (Count max. 5 tokens.)"),
        new PowerCard(ProductSet.JaggedEarth, Unique.ManyMindsMoveAsOne, "Pursue with Scratches, Pecks, and Stings", 0, Speed.Fast, new Ranges(Source.Presence, 2), TargetProperty.Beasts, [Elements.Sun, Elements.Fire, Elements.Air, Elements.Animal], "Moro Rogers", "1 Fear. For each Beasts past the first, Push 1 Explorer / Town."),
        new PowerCard(ProductSet.JaggedEarth, Unique.ManyMindsMoveAsOne, "A Dreadful Tide of Scurrying Flesh", 0, Speed.Fast, new Ranges(Source.SacredSite, 1), TargetProperty.TwoBeasts, [Elements.Moon, Elements.Air, Elements.Water, Elements.Animal], "Moro Rogers", "Remove up to half (round down) of Beasts in target land. For each Beasts Removed, 2 Fear and skip one Invader Action."),
        new PowerCard(ProductSet.JaggedEarth, Unique.ManyMindsMoveAsOne, "Boon of Swarming Bedevilment", 0, Speed.Fast, null, TargetSpirit.Another, [Elements.Air, Elements.Water, Elements.Animal], "Moro Rogers", "For the rest of this turn, each of target Spirit's Presence grants Defend 1 in its land. Target Spirit may Push up to 1 of their Presence."),
        new PowerCard(ProductSet.JaggedEarth, Unique.ManyMindsMoveAsOne, "Guide the Way on Feathered Wings", 0, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Air, Elements.Animal], "Moro Rogers", "Move 1 Beasts up to two lands. As it moves, up to 2 Dahan may move with it, for part or all of the way. (The Beasts / Dahan may move to an adjacent land and then back.)"),
        new PowerCard(ProductSet.JaggedEarth, Unique.ManyMindsMoveAsOne, "Ever-Multiplying Swarm", 1, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Fire, Elements.Earth, Elements.Animal], "Moro Rogers", "Add 2 Beasts."),
        // Promo2
        // Uniques
        new PowerCard(ProductSet.Promo2, Unique.DownpourDrenchesTheWorld, "Foundations Sink into Mud", 1, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Water, Elements.Earth], "Damon Westenhofer", "2 damage to Town. If target land is Wetland, you may instead deal 1 Damage to each Town / City."),
        new PowerCard(ProductSet.Promo2, Unique.DownpourDrenchesTheWorld, "Gift of Abundance", 1, Speed.Fast, null, TargetSpirit.Another, [Elements.Sun, Elements.Air, Elements.Water, Elements.Plant], "Damon Westenhofer", "Target Spirit either gains 2 Energy, or may Repeat one Power Card this turn by paying its cost. Either you or target Spirit may add 1 Destroyed Presence to a Wetland where you have Presence."),
        new PowerCard(ProductSet.Promo2, Unique.DownpourDrenchesTheWorld, "Unbearable Deluge", 0, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Air, Elements.Water, Elements.Earth], "Damon Westenhofer", "1 fear. Push 2 Dahan. Defend 3. If target land is Wetland, Isolate it."),
        new PowerCard(ProductSet.Promo2, Unique.DownpourDrenchesTheWorld, "Dark Skies Loose a Stinging Rain", 1, Speed.Fast, new Ranges(Source.Presence, 1, [Land.Wetland]), LandAny, [Elements.Moon, Elements.Air, Elements.Water], "Damon Westenhofer", "Isolate target land. Push up to 1 Explorer and up to 2 Dahan."),
        new PowerCard(ProductSet.Promo2, Unique.FinderOfPathsUnseen, "Traveler's Boon", 0, Speed.Fast, null, TargetSpirit.Another, [Elements.Moon, Elements.Air, Elements.Water], "Moro Rogers", "Target spirit moves up to 3 of their Presence to one of your lands. They may move up to 1 Invader, 1 Dahan and 1 Beasts along with their Presence. (Total, not for each Presence.)"),
        new PowerCard(ProductSet.Promo2, Unique.FinderOfPathsUnseen, "Offer Passage Between Worlds", 1, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Moon, Elements.Air], "Moro Rogers", "Move up to 4 Dahan between target land and one of your lands. -or- The next time Dahan would be Destroyed in target land, Destroy 2 fewer Dahan."),
        new PowerCard(ProductSet.Promo2, Unique.FinderOfPathsUnseen, "Aid from the Spirit-Speakers", 2, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Fire, Elements.Air, Elements.Animal], "Moro Rogers", "For each Dahan, you may move 1 Invader / Dahan / Presence / Beasts to a land within 2 Range that has Dahan."),
        new PowerCard(ProductSet.Promo2, Unique.FinderOfPathsUnseen, "Paths Tied by Nature", 0, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Air, Elements.Earth, Elements.Plant], "Moro Rogers", "Move up to 2 Invaders / Dahan / Presence / Beasts to a land within 2 Range that has the same terrain."),
        new PowerCard(ProductSet.Promo2, Unique.FinderOfPathsUnseen, "Ways of Shore and Heartland", 1, Speed.Slow, new Ranges(Source.Presence, 2), LandAny, [Elements.Air, Elements.Water, Elements.Earth], "Moro Rogers", "Push up to 2 Invaders / Dahan / Presence / Beasts to a land that is also Coastal / Inland (whichever the target land is.)"),
        new PowerCard(ProductSet.Promo2, Unique.FinderOfPathsUnseen, "A Circuitous and Wending Journey", 0, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Moon, Elements.Air], "Moro Rogers", "Push up to half (round up) of Invaders from target land. Do likewise (separately) for Dahan, Presence, and Beasts."),
        // Horizons of Spirit Island
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.DevouringTeethLurkUnderfoot, "Ferocious Rampage", 2, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Fire, Elements.Animal], "Moro Rogers", "1 Fear. 3 Damage to Explorer / Town only. (+1 Damage to Explorer / Town from your \"Territorial Aggression\" Special Rule.)"),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.DevouringTeethLurkUnderfoot, "Gift of Furious Might", 1, Speed.Fast, null, TargetSpirit.Another, [Elements.Moon, Elements.Fire, Elements.Animal], "Moro Rogers", "Once this turn, Target Spirit may deal +3 Damage when using a Damage-dealing Power. (This adds +3 Damage total, even for a Power that Damages multiple Invaders or \"each Invader\".)"),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.DevouringTeethLurkUnderfoot, "Herd Towards the Lurking Maw", 1, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Water, Elements.Earth, Elements.Animal], "Moro Rogers", "1 Fear. Gather up to 1 Explorer / Town."),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.DevouringTeethLurkUnderfoot, "Mark Territory with Scars and Teeth", 2, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Sun, Elements.Earth, Elements.Animal], "Moro Rogers", "Defend 9. 2 Fear if Invaders are present. Push 2 Dahan."),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.EyesWatchFromTheTrees, "Boon of Watchful Guarding", 0, Speed.Fast, null, TargetSpirit.Any, [Elements.Earth, Elements.Plant, Elements.Animal], "Moro Rogers", "In one of Target Spirit's lands, Defend 4. Target Spirit may pay 1 Energy to instead Defend 8. (This Power Defends a single land, letting you use your Special Rule \"Dahan Trust the Watchers.\")"),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.EyesWatchFromTheTrees, "Eerie Noises and Moving Trees", 2, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Moon, Elements.Air, Elements.Plant], "Moro Rogers", "2 Fear. Push up to 2 Explorer / Town."),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.EyesWatchFromTheTrees, "Mysterious Abductions", 1, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Moon, Elements.Fire, Elements.Plant], "Moro Rogers", "1 Fear. 1 Damage."),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.EyesWatchFromTheTrees, "Whispered Guidance Through the Night", 0, Speed.Slow, new Ranges(Source.Presence, 1, [Land.Jungle]), LandAny, [Elements.Moon, Elements.Air, Elements.Plant], "Moro Rogers", "Gather up to 3 Dahan. If Invaders and Dahan are present, 1 Fear."),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.FathomlessMudOfTheSwamp, "Exaltation of Tangled Growth", 0, Speed.Slow, null, TargetSpirit.Another, [Elements.Water, Elements.Earth, Elements.Plant], "Moro Rogers", "Target Spirit may pay 1 Energy to gain a Power Card. You may pay 2 Energy to gain a Power Card."),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.FathomlessMudOfTheSwamp, "Foul Vapors and Fetid Muck", 0, Speed.Slow, new Ranges(Source.SacredSite, 2), TargetProperty.Invaders, [Elements.Fire, Elements.Air, Elements.Water, Elements.Earth], "Moro Rogers", "1 Fear. Push up to 2 Explorer"),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.FathomlessMudOfTheSwamp, "Intractable Thickets and Thorns", 2, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Moon, Elements.Water, Elements.Earth, Elements.Plant], "Moro Rogers", "1 Fear. Defend 5."),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.FathomlessMudOfTheSwamp, "Open Shifting Waterways", 1, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Moon, Elements.Water, Elements.Animal], "Moro Rogers", "Gather up to 2 Dahan. If Dahan and Invaders are present, 1 Fear and 1 Damage."),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.RisingHEatOfStoneAndSand, "Call on Herders for Aid", 1, Speed.Slow, new Ranges(Source.Presence, 2), LandAny, [Elements.Sun, Elements.Fire, Elements.Earth, Elements.Animal], "Lucas Durham", "Gather up to 2 Dahan. For each Dahan present, Push up to 1 Explorer / Town / Dahan."),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.RisingHEatOfStoneAndSand, "Gift of Searing Heat", 0, Speed.Fast, null, TargetSpirit.Another, [Elements.Sun, Elements.Fire, Elements.Air], "Lucas durham", "Target Spirit gains 2 Energy. -or- Target Spirit may pay 1 Energy to do 1 Damage in one of their lands."),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.RisingHEatOfStoneAndSand, "Stinging Sandstorm", 1, Speed.Slow, new Ranges(Source.Presence, 1), LandAny, [Elements.Fire, Elements.Air, Elements.Earth], "Lucas Durham", "Gather up to 1 of your Presence. 1 Fear and 1 Damage. (If this power makes a SacredSite, your Special Rule applies immediately, giving Invaders there -1 Health and possibly Destroying Damaged Invaders.)"),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.RisingHEatOfStoneAndSand, "Sweltering Exhaustion", 2, Speed.Fast, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Fire, Elements.Air], "Lucas Durham", "1 Fear. Skip up to 1 Ravage / Build Action."),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.SunBrightWhirlwind, "Gift of the Sunlit Air", 0, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Fire, Elements.Air], "Lucas Durham", "Target Spirit gets +1 Range with all their Powers. If you target another Spirit, they gain 1 Energy."),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.SunBrightWhirlwind, "Gift of Wind-Sped Steps", 1, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Air, Elements.Animal], "Lucas Durham", "Once this turn, Target Spirit may choose 1 of their Slow Powers with a \"Push\" or \"Gather\" instruction and make that Power Fast (for this turn). If you target another Spirit, they gain 1 Energy."),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.SunBrightWhirlwind, "Scatter to the Winds", 1, Speed.Slow, new Ranges(Source.Presence, 2), LandAny, [Elements.Fire, Elements.Air, Elements.Water], "Lucas Durham", "Choose up to 5 Explorer / Town / Dahan. Push them to as many different lands as possible."),
        new PowerCard(ProductSet.HorizonsOfSpiritIsland, Unique.SunBrightWhirlwind, "Tempest of Leaves and Branches", 2, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Sun, Elements.Air, Elements.Plant], "Lucas Durham", "Choose up to 5 different Invaders (in target land). 1 Damage to each of them."),
        // Nature Incarnate
        // Majors
        new PowerCard(ProductSet.NatureIncarnate, PowerDeckType.Major, "Bargain of Coursing Paths", 2, Speed.Fast, new Ranges(Source.Presence, 0), TargetProperty.TwoDahan, [Elements.Moon, Elements.Air, Elements.Water, Elements.Earth], "Agnieszka Dąbrowiecka", "Bargain: 1 Presence now and -1 Energy / turn. Now: Mark both target land and another land with 2 or more Dahan. Ongoing: After pieces are added or moved into the marked lands: choose any land, then Move those pieces directly to that land. -If you have- 3 Air, 2 Water, 2 Earth: The Presence cost comes from your Presence tracks."),
        new PowerCard(ProductSet.NatureIncarnate, PowerDeckType.Major, "Bombard with Boulders and Stinging Seeds", 2, Speed.Slow, new Ranges(Source.Presence, 2, [Land.Mountain, Land.Jungle]), LandAny, [Elements.Air, Elements.Earth, Elements.Plant], "Kat Guevara", "1 Fear. 2 Damage. Add 1 Badlands. -If you have- 2 Air, 2 Earth, 3 Plant: 1 Fear. 2 Damage. Add 1 Wilds."),
        new PowerCard(ProductSet.NatureIncarnate, PowerDeckType.Major, "Exaltation of the Incandescent Sky", 7, Speed.Fast, null, TargetSpirit.Another, [Elements.Sun, Elements.Fire, Elements.Air, Elements.Water], "Kat Guevara", "Target Spirit may play 1 Power Card by paying its cost, make up to 2 of their Powers Fast this turn, and do 3 Damage in one of their lands. You may do likewise. -If you have- 3 Sun, 3 Fire, 4 Air, 2 Water: In any 4 lands of the island, Skip 1 Invader Action. 5 Fear (total)."),
        new PowerCard(ProductSet.NatureIncarnate, PowerDeckType.Major, "Flocking Red-Talons", 3, Speed.Fast, new Ranges(Source.Presence, 3, [Land.Wetland]), LandAny, [Elements.Air, Elements.Water, Elements.Plant, Elements.Animal], "Kat Guevara", "Add 1 Beasts. Move up to 2 Beasts within 3 Range to target land. For each Beasts presents, choose a different Invader. 1 Damage to each of those Invaders. Push 1 Explorer / Town per Beasts. -If you have- 2 Air, 2 Plant, 3 Animal: Repeat this Power on a different land within 3 Range (of target land)."),
        new PowerCard(ProductSet.NatureIncarnate, PowerDeckType.Major, "Fragments of Yesteryear", 7, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Sun, Elements.Moon], "David Markiwsky", "Remove all pieces, then Add the pieces matching target land's Setup symbols. -If you have- 3 Sun: This power may be Fast. 3 Moon: Don't remove Dahan, any Spirit's Presence, or Spirit Tokens. Don't add Invaders / Blight."),
        new PowerCard(ProductSet.NatureIncarnate, PowerDeckType.Major, "Inspire the Release of Stolen Lands", 4, Speed.Slow, new Ranges(Source.Presence, 2), TargetProperty.NoBlight, [Elements.Sun, Elements.Water, Elements.Plant, Elements.Animal], "Agnieszka Dąbrowiecka", "Gather up to 3 Dahan. Remove up to 3 Health worth of Invaders per Dahan. -If you have- 3 Sun, 3 Water, 2 Animal: This Power can target lands with Blight. If Dahan are present, Remove 1 Blight from target land, then Remove 1 Explorer, 1 Town, and 1 City from a land within 1 Range (of target land)."),
        new PowerCard(ProductSet.NatureIncarnate, PowerDeckType.Major, "Plague Ships Sail to Distant Ports", 4, Speed.Fast, new Ranges(Source.Presence, 1), [Land.Coastal, TargetProperty.City], [Elements.Fire, Elements.Air, Elements.Water, Elements.Animal], "Kat Guevara", "1 Fear. Add 4 Disease among Coastal lands (on any boards) other than target land. -If you have- 2 Fire, 2 Water, 2 Animal: Instead: 1 Fear. 3 Damage. Spirits may jointly spend 3 Energy per player (aided by removing Disease from the island for 3 Energy each) to remove the top card of the Fear Deck from the game. Add 1 Disease."),
        new PowerCard(ProductSet.NatureIncarnate, PowerDeckType.Major, "Ravaged Undergrowth Slithers Back to Life", 3, Speed.Slow, new Ranges(Source.SacredSite, 1), TargetProperty.Blight, [Elements.Water, Elements.Plant, Elements.Animal], "Kat Guevara", "Replace 1 Blight with 1 Wilds. 1 Fear. 3 Damage. Push that Wilds. -If you have- 3 Water, 2 Plant: Add 1 Wilds. You may Push it. In each land with Wilds within 1 Range (of target land): Push 1 Explorer and 1 Town to lands without Wilds."),
        new PowerCard(ProductSet.NatureIncarnate, PowerDeckType.Major, "Rumbling Earthquakes", 6, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Fire, Elements.Earth], "Emily Hancock", "This Power ignores Health bonuses. 3 Fear. 6 Damage, to Town / City only. 6 Damage among adjacent lands, to Town / City only. -If you have- 4 Earth: 6 Damage among target / adjacent lands, to Town / City only."),
        new PowerCard(ProductSet.NatureIncarnate, PowerDeckType.Major, "Solidify Echoes of Majesty Past", 4, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Moon, Elements.Air, Elements.Earth], "Emily Hancock", "Choose one of target Spirit's lands. In that land and each adjacent land, Defend 3. They Add 1 Destroyed Presence to each adjacent land. Skip up to 1 Invader Action at each added Destroyed Presence. -If you have- 2 Sun, 2 Moon, 2 Earth: Target Spirit either Reclaims 1 Power Card or re-gains a Unique Power they previously forgot. They may play it by paying its cost."),
        new PowerCard(ProductSet.NatureIncarnate, PowerDeckType.Major, "Transformative Sacrifice", 3, Speed.Fast, null, TargetSpirit.Any, [Elements.Moon, Elements.Fire, Elements.Water, Elements.Plant], "Kat Guevara", "Target Spirit may Remove up to 3 Presence (from anywhere on the island). Then for each removed Presence, they Take a Minor Power and play it (for free). -If you have- 2 Moon, 3 Fire, 2 Plant: Before taking cards, they may also Remove 1 Presence from their Presence track to Take a Minor Power and play it."),
        new PowerCard(ProductSet.NatureIncarnate, PowerDeckType.Major, "Unearth a Beast of Wrathful Stone", 5, Speed.Fast, new Ranges(Source.SacredSite, 1), TargetProperty.Invaders, [Elements.Moon, Elements.Fire, Elements.Earth, Elements.Animal], "David Markiwsky", "After the next Invader Phase (on any turn) with no Ravage / Build Actions in target land: 3 Fear. 12 Damage. Add 1 Beasts. You may Push that Beasts. 1 Fear and 2 Damage in its land. -If you have- 2 Moon, 3 Earth, 3 Animal: Mark it (Marked). Marked can't leave the island. Each Slow Phase: You may Push Marked. 1 Fear and 2 Damage at Marked."),
        // Minors
        new PowerCard(ProductSet.NatureIncarnate, PowerDeckType.Minor, "Roiling Bog and Snagging Thorn", 0, Speed.Fast, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Moon, Elements.Fire, Elements.Water, Elements.Plant], "Kat Guevara", "1 Fear. Isolate. Defend 2. 1 Dahan does not participate in Ravage. (Check when ravaging; it does not take Damage and does not counterattack.)"),
        // Uniques
        new PowerCard(ProductSet.NatureIncarnate, Unique.BreathOfDarknessDownYourSpine, "Emerge from the Dread Night Wind", 1, Speed.Slow, null, LandAny, [Elements.Moon, Elements.Air], "David Markiwsky", "Add / Move Incarna to target land. 1 Fear. If exactly 1 Invader is present, Abduct it. Otherwise, Push up to 2 Explorer / Town to different lands. Push up to 2 Dahan."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.BreathOfDarknessDownYourSpine, "Reach from the Infinite Darkness", 0, Speed.Fast, null, TargetSpirit.Yourself, [Elements.Moon, Elements.Air, Elements.Animal], "David Markiwsky", "Abduct up to 2 Presence (of any Spirits, with their permission) from any lands on the island, ignoring land type restrictions on moving Presence. Each Spirit's Presence in Endless Dark grants them +1 Range with all their Powers (this turn)."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.BreathOfDarknessDownYourSpine, "Swallowed by the Endless Dark", 1, Speed.Fast, new Ranges(Source.Presence, 0), TargetProperty.Invaders, [Elements.Moon, Elements.Air, Elements.Water], "David Markiwsky", "2 Fear. Abduct 1 Explorer. -If you have- 3 Moon, 3 Air: Abduct 1 Invader."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.BreathOfDarknessDownYourSpine, "Terror of the Hunted", 1, Speed.Slow, new Ranges(Source.Presence, 0), TargetProperty.Invaders, [Elements.Moon, Elements.Fire, Elements.Animal], "David Markiwsky", "If Beasts are present, 1 Fear and Add 1 Strife. Add 1 Strife per Terror Level. If target land is Endless Dark, Add 1 Strife. (Strife only escapes with the Invader it's attached to.)"),
        new PowerCard(ProductSet.NatureIncarnate, Unique.DancesUpEarthquakes, "Inspire a Winding Dance", 0, Speed.Slow, new Ranges(Source.Presence, 1), TargetProperty.Invaders, [Elements.Moon, Elements.Water, Elements.Earth, Elements.Animal], "Emily Hancock", "Push up to 1 Explorer / Town. Gather up to 1 Dahan."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.DancesUpEarthquakes, "Exaltation of Echoed Steps", 1, Speed.Slow, null, TargetSpirit.Another, [Elements.Moon, Elements.Water, Elements.Earth], "Emily Hancock", "Target Spirit may Push 1 Presence, Bringing up to 1 Explorer / Town / Dahan / Beasts. You may do likewise."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.DancesUpEarthquakes, "Gift of Seismic Energy", 3, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Fire, Elements.Earth, Elements.Plant], "Emily Hancock", "If you target yourself, gain 3 Energy. Otherwise, target Spirit gains 1 Energy per Power Card you have in play (max. 6). (Don't count Impending Card.)"),
        new PowerCard(ProductSet.NatureIncarnate, Unique.DancesUpEarthquakes, "Radiating Tremors", 2, Speed.Slow, new Ranges(Source.Presence, 0), LandAny, [Elements.Moon, Elements.Fire, Elements.Earth], "Emily Hancock", "2 Damage. You may Push any number of Quake, dividing them as evenly as possible between adjacent lands."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.DancesUpEarthquakes, "Resounding Footfalls Sow Dismay", 3, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Fire, Elements.Air, Elements.Earth], "Emily Hancock", "1 Fear. Add 1 Quake. Skip all Ravage Actions."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.DancesUpEarthquakes, "Rumblings Portend a Greater Quake", 1, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Sun, Elements.Moon, Elements.Air, Elements.Earth], "Emily Hancock", "If you have at least as many Impending Card as Power Cards in play, 1 Fear and Add 1 Quake. Push up to 3 Dahan."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.EmberEyedBehemoth, "Blazing Intimidation", 2, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Fire, Elements.Plant, Elements.Animal], "David Markiwsky", "1 Fear. Push 2 Explorer / Town to a land without Incarna."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.EmberEyedBehemoth, "Exaltation of Grasping Roots", 0, Speed.Slow, null, TargetSpirit.Another, [Elements.Moon, Elements.Fire, Elements.Earth, Elements.Plant], "David Markiwsky", "Target Spirit may Add 1 Wilds in one of their lands. You may do likewise."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.EmberEyedBehemoth, "Surging Lahar", 2, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Fire, Elements.Water, Elements.Earth], "David Markiwsky", "2 Damage. If your Presence is present, Add 1 Badlands."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.EmberEyedBehemoth, "Terrifying Rampage", 1, Speed.Fast, new Ranges(Source.Presence, 1), LandAny, [Elements.Moon, Elements.Fire, Elements.Earth], "David Markiwsky", "1 Fear. 2 Invaders don't participate in Ravage. (Choose the Invaders when ravaging; they don't deal Damage or take counterattack Damage.) Push 3 Dahan."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.HearthVigil, "Call to Vigilance", 2, Speed.Slow, new Ranges(Source.Presence, 1, undefined, TargetProperty.Dahan), LandAny, [Elements.Sun, Elements.Air, Elements.Animal], "Aalaa Yassin", "2 Fear if Invaders are present. For each Dahan in origin land, Push up to 1 Explorer / Town."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.HearthVigil, "Coordinated Raid", 1, Speed.Slow, new Ranges(Source.Presence, 1, undefined, TargetProperty.Dahan), LandAny, [Elements.Sun, Elements.Earth, Elements.Animal], "Aalaa Yassin", "1 Damage. If Dahan are present, 1 Damage."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.HearthVigil, "Favors of Story and Season", 1, Speed.Fast, null, TargetSpirit.Another, [Elements.Sun, Elements.Earth, Elements.Plant, Elements.Animal], "Aalaa Yassin", "Target Spirit may Gather up to 3 Dahan into one of their lands. If they have at least 3 Dahan among their lands, they gain 1 Energy and may Reclaim 1 Power Card instead of discarding it at the end of turn."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.HearthVigil, "Surrounded by the Dahan", 0, Speed.Fast, new Ranges(Source.Presence, 0), TargetProperty.Dahan, [Elements.Moon, Elements.Air, Elements.Animal], "Aalaa Yassin", "2 Fear if Invaders are present. 1 Fear if Dahan outnumber Town / City. Isolate target land."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.RelentlessGazeOfTheSun, "Blinding Glare", 0, Speed.Fast, new Ranges(Source.SacredSite, 0), TargetProperty.Invaders, [Elements.Sun, Elements.Air], "Agnieszka Dąbrowiecka", "2 Fear. -or- Skip up to one Ravage Action. -If you have- 5 Sun: Instead, 3 Fear. -or- Skip to one Invader Action."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.RelentlessGazeOfTheSun, "Focus the Sun's Rays", 0, Speed.Slow, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Sun, Elements.Fire, Elements.Air], "Agnieszka Dąbrowiecka", "1 Damage. 2 Damage to Dahan. Move up to 3 Presence directly to target land (from anywhere on the island). You may Bring 1 Badlands (total) with those Presence."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.RelentlessGazeOfTheSun, "Unbearable Gaze", 1, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Sun, Elements.Fire], "Agnieszka Dąbrowiecka", "1 Fear. Push 2 Explorer / Town from origin or target land (or 1 Explorer / Town from each)."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.RelentlessGazeOfTheSun, "Wither Bodies, Scar Stones", 1, Speed.Slow, new Ranges(Source.SacredSite, 2), LandAny, [Elements.Sun, Elements.Fire, Elements.Earth], "Agnieszka Dąbrowiecka", "1 Damage. -or- Add 1 Badlands."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.ToweringRootsOfTheJungle, "Blooming of the Rocks and Trees", 0, Speed.Slow, new Ranges(Source.SacredSite, 1), LandAny, [Elements.Sun, Elements.Air, Elements.Earth, Elements.Plant], "Aalaa Yassin", "If no Blight is present, Add 1 Vitality. -or- If no Invaders are present, Add 1 Wilds. -If you have- 3 Plant: You may do both."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.ToweringRootsOfTheJungle, "Boon of Resilient Power", 1, Speed.Slow, null, TargetSpirit.Any, [Elements.Sun, Elements.Moon, Elements.Water, Elements.Plant], "Aalaa Yassin", "Target Spirit may Add 1 Destroyed Presence to one of your lands. If you target yourself, gain a Major Power. Otherwise, target Spirits gains a Power Card."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.ToweringRootsOfTheJungle, "Entwine the Fates of All", 1, Speed.Fast, null, TargetSpirit.Any, [Elements.Moon, Elements.Water, Elements.Earth, Elements.Plant], "Aalaa Yassin", "In one of target Spirit's lands, Defend 2 per Presence (from all Spirits)."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.ToweringRootsOfTheJungle, "Radiant and Hallowed Grove", 2, Speed.Fast, null, TargetProperty.Incarna, [Elements.Sun, Elements.Moon, Elements.Fire, Elements.Plant], "Aalaa Yassin", "2 Fear if Invaders are present or adjacent. In both target and one adjacent land, you may Remove an Invader with Health less than or equal to the Terror Level. (Damage doesn't reduce Health.)"),
        new PowerCard(ProductSet.NatureIncarnate, Unique.WanderingVoiceKeensDelirium, "Exhale Confusion and Delirium", 0, Speed.Fast, new Ranges(Source.Presence, 1), TargetProperty.Strife, [Elements.Sun, Elements.Animal, Elements.Air, Elements.Animal], "Emily Hancock", "2 Fear. Invaders with Strife don't participate in Ravage. (Check when ravaging; they don't deal Damage or take counterattack Damage.)"),
        new PowerCard(ProductSet.NatureIncarnate, Unique.WanderingVoiceKeensDelirium, "Frightful Keening", 1, Speed.Slow, null, TargetProperty.Incarna, [Elements.Sun, Elements.Fire, Elements.Air], "Emily Hancock", "Push Incarna. If this pushes Incarna into a land with Invaders, 2 Fear there (before adding Strife)."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.WanderingVoiceKeensDelirium, "Turmoil's Touch", 0, Speed.Slow, null, TargetSpirit.Another, [Elements.Sun, Elements.Moon, Elements.Air, Elements.Plant], "Emily Hancock", "Target Spirit may either pay 1 Energy or discard a Power Card (from hand) to Take a Minor Power into their discard. You may do likewise"),
        new PowerCard(ProductSet.NatureIncarnate, Unique.WanderingVoiceKeensDelirium, "Twist Perceptions", 1, Speed.Slow, new Ranges(Source.Presence, 1), TargetProperty.Invaders, [Elements.Animal, Elements.Air, Elements.Animal], "Emily Hancock", "Add 1 Strife. You may Push the Invader you added Strife to. (If you add Strife to Explorer / Town, you can push that Invader first with Senseless Roaming before pushing it with this Power.)"),
        new PowerCard(ProductSet.NatureIncarnate, Unique.WoundedWatersBleeding, "Blood Water and Bloodlust", 1, Speed.Slow, new Ranges(Source.Presence, 1, undefined, TargetProperty.Blight), LandAny, [Elements.Fire, Elements.Water, Elements.Animal], "Nolan Nasser", "Add 1 Beasts and 1 Disease."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.WoundedWatersBleeding, "Boon of Corrupted Blood", 1, Speed.Fast, null, TargetSpirit.Any, [Elements.Sun, Elements.Fire, Elements.Animal], "Nolan Nasser", "1 Damage in one of target Spirit's lands. If you target another Spirit, in that land also: Destroy 1 of their Presence. 1 Damage. Gather 1 Beasts."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.WoundedWatersBleeding, "Draw to the Water's Edge", 1, Speed.Fast, new Ranges(Source.Presence, 0), LandAny, [Elements.Sun, Elements.Water, Elements.Plant], "Nolan Nasser", "Gather up to 2 Town from a single land."),
        new PowerCard(ProductSet.NatureIncarnate, Unique.WoundedWatersBleeding, "Wrack with Pain and Grief", 1, Speed.Slow, new Ranges(Source.Presence, 1, undefined, TargetProperty.Blight), TargetProperty.Invaders, [Elements.Water, Elements.Plant, Elements.Animal], "Nolan Nasser", "2 Fear. Push 1 Explorer and 1 Town."),
        // Fear Cards
        // Basegame
        new FearCard(ProductSet.Basegame, FearType.Fear, "Fear of the Unseen", "Each player removes 1 Explorer / Town from a land with SacredSite.", "Each player removes 1 Explorer / Town from a land with Presence.", "Each player removes 1 Explorer / Town from a land with Presence, or 1 City from a land with SacredSite."),
        new FearCard(ProductSet.Basegame, FearType.Fear, "Scapegoats", "Each Town destroys 1 Explorer in its land.", "Each Town destroys 1 Explorer in its land. Each City destroys 2 Explorer in its land.", "Destroy all Explorer in lands with Town / City. Each City destroys 1 Town in its land."),
        new FearCard(ProductSet.Basegame, FearType.Fear, "Emigration Accelerates", "Each player removes 1 Explorer from a Coastal land.", "Each player removes 1 Explorer / Town from a Coastal land.", "Each player removes 1 Explorer / Town from any land."),
        new FearCard(ProductSet.Basegame, FearType.Fear, "Dahan on their Guard", "In each land, Defend 1 per Dahan.", "In each land with Dahan, Defend 1, plus an additional Defend 1 per Dahan.", "In each land, Defend 2 per Dahan."),
        new FearCard(ProductSet.Basegame, FearType.Fear, "Tall Tales of Savagery", "Each player removes 1 Explorer from a land with Dahan.", "Each player removes 2 Explorer or 1 Town from a land with Dahan.", "Remove 2 Explorer or 1 Town from each land with Dahan. Then, remove 1 City from each land with at least 2 Dahan."),
        new FearCard(ProductSet.Basegame, FearType.Fear, "Retreat!", "Each player may Push up to 2 Explorer from an Inland land.", "Each player may Push up to 3 Explorer / Town from an Inland land.", "Each player may Push any number of Explorer / Town from one land."),
        new FearCard(ProductSet.Basegame, FearType.Fear, "Dahan Raid", "Each player chooses a different land with Dahan. 1 Damage there.", "Each player chooses a different land with Dahan. 1 Damage per Dahan there.", "Each player chooses a different land with Dahan. 2 Damage per Dahan there."),
        new FearCard(ProductSet.Basegame, FearType.Fear, "Dahan Enheartened", "Each player may Push 1 Dahan from a land with Invaders or Gather 1 Dahan into a land with Invaders.", "Each player chooses a different land. In chosen lands: Gather up to 2 Dahan, then 1 Damage if Dahan are present.", "Each player chooses a different land. In chosen lands: Gather up to 2 Dahan, then 1 Damage per Dahan present."),
        new FearCard(ProductSet.Basegame, FearType.Fear, "Avoid the Dahan", "Invaders do not Explore into lands with at least 2 Dahan.", "Invaders do not Build in lands where Dahan outnumber Town / City.", "Invaders do not Build in lands with Dahan."),
        new FearCard(ProductSet.Basegame, FearType.Fear, "Seek Safety", "Each player may Push 1 Explorer into a land with more Town / City than the land it came from.", "Each player may Gather 1 Explorer into a land with Town / City, or Gather 1 Town into a land with City.", "Each player may remove up to 3 Health worth of Invaders from a land without City."),
        new FearCard(ProductSet.Basegame, FearType.Fear, "Wary of the Interior", "Each player removes 1 Explorer from an Inland land.", "Each player removes 1 Explorer / Town from an Inland land.", "Each player removes 1 Explorer / Town from any land."),
        new FearCard(ProductSet.Basegame, FearType.Fear, "Belief Takes Root", "Defend 2 in all lands with Presence.", "Defend 2 in all lands with Presence. Each Spirit gains 1 Energy per SacredSite they have in lands with Invaders.", "Each player chooses a different land and removes up to 2 Health worth of Invaders per Presence there."),
        new FearCard(ProductSet.Basegame, FearType.Fear, "Isolation", "Each player removes 1 Explorer / Town from a land where it is the only Invader.", "Each player removes 1 Explorer / Town from a land with 2 or fewer Invaders.", "Each player removes an Invader from a land with 2 or fewer Invaders."),
        new FearCard(ProductSet.Basegame, FearType.Fear, "Overseas Trade Seem Safer", "Defend 3 in all Coastal lands.", "Defend 6 in all Coastal lands. Invaders do not Build City in Coastal lands this turn.", "Defend 9 in all Coastal lands. Invaders do not Build in Coastal lands this turn."),
        new FearCard(ProductSet.Basegame, FearType.Fear, "Trade Suffers", "Invaders do not Build in lands with City.", "Each player may replace 1 Town with 1 Explorer in a Coastal land.", "Each player may replace 1 City with 1 Town or 1 Town with 1 Explorer in a Coastal land."),
        // Branch & Claw
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Demoralized", "Defend 1 in all lands.", "Defend 2 in all lands.", "Defend 3 in all lands."),
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Plan for Departure", "Each player may Gather 1 Town into a Coastal land.", "Each player may Gather 1 Explorer / Town into a Coastal land. Defend 2 in all Coastal lands.", "Each player may Gather up to 2 Explorer / Town into a Coastal land. Defend 4 in all Coastal lands."),
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Tread Carefully", "Each player may choose a land with Dahan or adjacent to at least 5 Dahan. Invaders do not Ravage there this turn.", "Each player may choose a land with Dahan or adjacent to at least 3 Dahan. Invaders do not Ravage there this turn.", "Each player may choose a land with Dahan or adjacent to Dahan. Invaders do not Ravage there this turn."),
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Dahan Attack", "Each player removes 1 Explorer from a land with Dahan.", "Each player chooses a different land with Dahan. 1 Damager per Dahan there.", "Each player chooses a different land with Town / City. Gather 1 Dahan into that land. Then, 2 Damage per Dahan there."),
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Explorers are Reluctant", "During the next normal Explore, skip the lowest-numbered land matching the Invader Card on each board.", "Skip the next normal Explore. During the next invader Phase, draw an additional Explore card.", "Skip the next normal Explore, but still reveal a card. (Perform the Escalation if relevant.) Cards shift left as usual."),
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Immigration Slows", "During the next normal Build, skip the lowest-numbered land matching the Invader Card on each board.", "Skip the next normal Build. The Build Card remains in place instead of shifting left.", "Skip the next normal Build. The Build Card shifts left as usual."),
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Flee the Pestilent Land", "Each player removes 1 Explorer / Town from a land with Disease.", "Each player removes up to 3 Health of Invaders from a land with Disease or 1 Explorer from an Inland land.", "Each player removes up to 5 Health of Invaders from a land with Disease, or 1 Explorer / Town from an Inland land."),
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Quarantine", "Explore does not affect Coastal lands.", "Explore does not affect Coastal lands. Lands with Disease are not a source of Invaders when Exploring.", "Explore does not affect Coastal lands. Invaders do not act in lands with Disease."),
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Too Many Monsters", "Each player removes 1 Explorer / Town from a land with Beasts.", "Each player removes 1 Explorer and 1 Town from a land with Beasts, or 1 Explorer from a land adjacent to Beasts.", "Each player removes 2 Explorer and 2 Town from a land with Beasts or 1 Explorer / Town from a land adjacent to Beasts."),
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Panicked by Wild Beasts", "Each player adds 1 Strife in a land with or adjacent to Beasts.", "Each player adds 1 Strife in a land with or adjacent to Beasts. Invaders skip their normal Explore and Build in lands with Beasts.", "Each player adds 1 Strife in a land with or adjacent to Beasts. Invaders skip all normal Actions in lands with Beasts."),
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Depart the Dangerous Land", "Each player removes 1 Explorer from a land with Beasts, Disease, or at least 2 Dahan.", "Each player removes 1 Explorer / town from a land with Beasts, Disease, or at least 2 Dahan.", "Each player removes up to 4 Health worth of Invaders from a land with Beasts, Disease, or at least 2 Dahan."),
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Unrest", "Each player adds 1 Strife to a Town.", "Each player adds 1 Strife to a Town. For the rest of this turn, Invaders have -1 Health per Strife to a minimum of 1.", "Each player adds 1 Strife to an Invader. For the rest of this turn, Invaders have -1 Health per Strife to a minimum of 1."),
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Panic", "Each player adds 1 Strife in a land with Beasts / Disease / Dahan.", "Each player adds 1 Strife in a land with Beasts / Disease / Dahan. For the rest of this turn, Invaders have -1 Health per Strife to a minimum of 1.", "Each player adds 1 Strife to an Invader. For the rest of this turn, Invaders have -1 Health per Strife to a minimum of 1."),
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Discord", "Each player adds 1 Strife in a different land with at least 2 Invaders.", "Each player adds 1 Strife in a different land with at least 2 Invaders. Then, each Invader takes 1 Damage per Strife it has.", "Each player adds 1 Strife in a different land with at least 2 Invaders. Then, each Invader with Strife deals Damage to other Invaders in its land."),
        new FearCard(ProductSet.BranchAndClaw, FearType.Fear, "Dahan Threaten", "Each player adds 1 Strife in a land with Dahan.", "Each player adds 1 Strife in a land with Dahan. For the rest of this turn, Invaders have -1 Health per Strife to a minimum of 1.", "Each player adds 1 Strife in a land with Dahan. In every land with Strife, 1 Damage per Dahan."),
        // Jagged Earth
        new FearCard(ProductSet.JaggedEarth, FearType.Fear, "Sense of Dread", "Terror Level 1: On Each Board: Remove 1 Explorer from a land matching a Ravage card.", "Terror Level 2: On Each Board: Remove 1 Explorer / Town from a land matching a Ravage card.", "Terror Level 3: On Each Board: Remove 1 Invader from a land matching a Ravage card."),
        new FearCard(ProductSet.JaggedEarth, FearType.Fear, "Flee from Dangerous Lands", "Terror Level 1: On Each Board: Push 1 Explorer / Town from a land with Badlands / Wilds / Dahan.", "Terror Level 2: On Each Board: Remove 1 Explorer / Town from a land with Badlands / Wilds / Dahan.", "Terror Level 3: On Each Board: Remove 1 Explorer / Town from any land, or Remove 1 City from a land with Badlands / Wilds / Dahan."),
        new FearCard(ProductSet.JaggedEarth, FearType.Fear, "Dahan Reclaim Fishing Grounds", "Terror Level 1: Each player chooses a different Coastal land with Dahan. In each: 1 Damage per Dahan.", "Terror Level 2: Each player chooses a different Coastal land. In each: Gather up to 1 Dahan. 1 Damage per Dahan.", "Terror Level 3: Each player chooses a different Coastal land. In each: Gather up to 1 Dahan. 2 Damage per Dahan."),
        new FearCard(ProductSet.JaggedEarth, FearType.Fear, "Beset by Many Troubles", "Terror Level 1: In each land with Badlands / Beasts / Disease / Wilds / Strife, Defend 3.", "Terror Level 2: In each land with Badlands / Beasts / Disease / Wilds / Strife, or adjacent to 3 or more such tokens, Defend 5.", "Terror Level 3: Every Badlands / Beasts / Disease / Wilds / Strife grants Defend 3 in its land and adjacent lands."),
        new FearCard(ProductSet.JaggedEarth, FearType.Fear, "Nerves Fray", "Terror Level 1: Each player adds 1 Strife in a land not matching a Ravage Card.", "Terror Level 2: Each player adds 2 Strife in a single land not matching a Ravage Card.", "Terror Level 3: Each player adds 2 Strife in a single land not matching a Ravage Card. 1 Fear per player."),
        new FearCard(ProductSet.JaggedEarth, FearType.Fear, "Theological Strife", "Terror Level 1: Each player adds 1 Strife in a land with Presence.", "Terror Level 2: Each player adds 1 Strife in a land with Presence. Each Spirit gains 1 Energy per SacredSite they have in lands with Invaders.", "Terror Level 3: Each player adds 1 Strife in a land with Presence. Then, each Invader with Strife deals Damage to other Invaders in its land."),
        // Promo2
        new FearCard(ProductSet.Promo2, FearType.Fear, "Angry Mobs", "Terror Level 1: Each player may replace 1 Town with 2 Explorer. 1 Fear per player who does.", "Terror Level 2: In each land with 2 or more Explorer, destroy 1 Explorer / Town per 2 Explorer.", "Terror Level 3: In each land with 2 or more Explorer, destroy 1 Invader per 2 Explorer."),
        new FearCard(ProductSet.Promo2, FearType.Fear, "Mimic the Dahan", "Terror Level 1: Each player removes 1 Explorer / Town from a land with 2 or more Dahan.", "Terror Level 2: Each player replaces 1 Explorer / Town with 1 Dahan in a land with 2 or more Dahan.", "Terror Level 3: Each player replaces 1 Explorer / Town with 1 Dahan in a land with Dahan, or adjacent to 3 or more Dahan."),
        new FearCard(ProductSet.Promo2, FearType.Fear, "Depopulation", "Terror Level 1: On Each Board: Replace 1 Town with 1 Explorer.", "Terror Level 2: On Each Board: Remove 1 Town.", "Terror Level 3: On Each Board: Remove 1 Town, or Replace 1 City with 1 Town."),
        new FearCard(ProductSet.Promo2, FearType.Fear, "Communities in Disarray", "Terror Level 1: City each deal -1 Damage during Ravage. Invaders do not heal Damage at the end of this turn.", "Terror Level 2: Town / City each deal -1 Damage during Ravage. Invaders do not heal Damage at the end of this turn.", "Terror Level 3: Town / City each deal -2 Damage during Ravage. Invaders do not heal Damage at the end of this turn."),
        new FearCard(ProductSet.Promo2, FearType.Fear, "Spreading Timidity", "Terror Level 1: Each player chooses a land to Isolate.", "Terror Level 2: Each player chooses a different land to Isolate. Also, Defend 2 in those lands.", "Terror Level 3: Each player chooses a different land to Isolate. Also, Defend 4 in those lands."),
        // Nature Incarnate
        new FearCard(ProductSet.NatureIncarnate, FearType.Fear, "Civil Unrest", "Terror Level 1: On Each Board: Add 1 Strife to a Town / City in a land not matching a Ravage Card.", "Terror Level 2: On Each Board: Add 1 Strife to a Town / City in a land not matching a Ravage Card. Each Invader takes 1 Damage per Strife it has.", "Terror Level 3: On Each Board: Add 1 Strife. Each Invader takes 1 Damage per Strife it has."),
        new FearCard(ProductSet.NatureIncarnate, FearType.Fear, "Dahan Gain the Edge", "Terror Level 1: Each player chooses a different land with Dahan. In Each: Defend 2.", "Terror Level 2: Each player chooses a different land with Dahan. In Each: 1 Damage and Defend 3.", "Terror Level 3: Each player chooses a different land with Dahan. In Each: 2 Damage and Defend 4."),
        new FearCard(ProductSet.NatureIncarnate, FearType.Fear, "Daunted by the Dahan", "Terror Level 1: 1 Fear per board with both Invaders and Dahan. Invaders do -6 Damage to Dahan (per land) during Ravage.", "Terror Level 2: 1 Fear per board with both Invaders and Dahan. Lands with Dahan have Defend 3. Invaders do -6 Damage to Dahan (per land) during Ravage.", "Terror Level 3: 1 Fear per board with both Invaders and Dahan. Lands with Dahan have Defend 3. Invaders do -6 Damage to Dahan (per land) during Ravage. Isolate all lands with Dahan."),
        new FearCard(ProductSet.NatureIncarnate, FearType.Fear, "Distracted by Local Troubles", "Terror Level 1: On Each Board, in a land matching a Ravage Card: 1 Damage.", "Terror Level 2: Invaders do -1 Damage per Damage they have taken. On Each Board, in a land matching a Ravage Card: 1 Damage each to up to 2 Invaders.", "Terror Level 3: Invaders do -1 Damage per Damage they have taken. On Each Board, in two lands matching a Ravage Card: 2 Damage (per land)."),
        new FearCard(ProductSet.NatureIncarnate, FearType.Fear, "Restlessness", "Terror Level 1: Each player Pushes up to 1 Explorer / Town from a land not matching a Build card.", "Terror Level 2: Each player Pushes up to 3 Explorer / Town from a land not matching a Build card.", "Terror Level 3: Each player Removes up to 3 Explorer / Town from a land not matching a Build card."),
        new FearCard(ProductSet.NatureIncarnate, FearType.Fear, "Seek Company", "Terror Level 1: On Each Board: Gather up to 1 Explorer into a land with 2 or more Invaders.", "Terror Level 2: On Each Board: Gather up to 3 Explorer / Town from a single land into a land with 2 or more Invaders.", "Terror Level 3: On Each Board: Gather up to 4 Explorer / Town (total) into lands with 2 or more Invaders."),
        new FearCard(ProductSet.NatureIncarnate, FearType.Fear, "Struggles over Farmland", "Terror Level 1: Each player Adds 1 Strife in a land with Blight.", "Terror Level 2: Each player Adds 1 Strife to a Town or Adds 1 Strife in a land with Blight.", "Terror Level 3: Each player Adds 1 Strife. In each land with Blight, 1 Invader with Strife does Damage to other Invaders."),
        new FearCard(ProductSet.NatureIncarnate, FearType.Fear, "Supply Chains Abandoned", "Terror Level 1: On Each Board: Isolate one land.", "Terror Level 2: On Each Board: Isolate one land. If Town / City are present, skip all Build Actions (in that land).", "Terror Level 3: On Each Board: Isolate two lands. In each of those lands, if Town / City are present, skip all Build Actions (in that land)."),
        new FearCard(ProductSet.NatureIncarnate, FearType.Fear, "Unsettled", "Terror Level 1: On Each Board: Choose a land with Beasts / Strife / Dahan. Downgrade 1 Town / City there.", "Terror Level 2: On Each Board: Choose a land with Beasts / Strife / Dahan. Downgrade 1 Town / City there ore skip the next Build Action there (this turn).", "Terror Level 3: On Each Board: Choose a land with Beasts / Strife / Dahan. Remove 1 Invader there or skip the next Build Action there (this turn)."),
        // Events
        // Branch & Claw
        new ChoiceEventCard(ProductSet.BranchAndClaw, "Years of Little Rain", "A terrible drought parches the island. You may:", null, [Events.LetThePlantsDieAndTheLandWither, Events.ActToEaseTheDrought], TokenEvent.BeastsAttack, DahanEvent.CannyDefense),
        new ChoiceEventCard(ProductSet.BranchAndClaw, "Farmers Seek the Dahan for Aid", "The Dahan are uncertain whether to teach the Invaders farming techniques more in tune with the island's life. You recommend they:", null, [Events.SpurnTheInvaders, Events.TeachTheInvaders], TokenEvent.NewDiseases, null),
        new ChoiceEventCard(ProductSet.BranchAndClaw, "New Species Spread", "New plants and animals brought by the Invaders damage the local ecology. You may:", null, [Events.LetTheInvasiveSpeciesBloom, Events.TransmuteTheWorstOfTheSpecies], TokenEvent.NewDiseases, DahanEvent.OfferingsOfPatternAndDance),
        new ChoiceEventCard(ProductSet.BranchAndClaw, "War Touches the Island's Shores", "Invaders from a different faraway land assault the ones here, torching farms and bombarding Cities. You may:", null, [Events.AllowTheAttacks, Events.HelpRepelTheNewcomers], TokenEvent.BeastsFindNewHomes, DahanEvent.ReclaimTerritory),
        new ChoiceEventCard(ProductSet.BranchAndClaw, "Sacred Sites under Threat", "Invaders have begun to find hidden places of natural power. You may:", null, [Events.LetTheIslandsStrengthRepulseThem, Events.GuardThemYourselfForWellOrIll], TokenEvent.BeastsProwl, DahanEvent.SpiritSpeakersSolveRiddlesOfPower),
        new ChoiceEventCard(ProductSet.BranchAndClaw, "Outpaced", "Humanity has always been faster than you, but the Invaders' terrifying speed catches you off-guard. Each Spirit chooses independently for each of their Slow Power Cards played this turn:", null, [Events.StaySteadyAndSlow, Events.WorkToMatchTheirPace], TokenEvent.LingeringPlagues, DahanEvent.RaidsInForce),
        new ChoiceEventCard(ProductSet.BranchAndClaw, "Missionaries Arrive", "They teach and spread lessons of a foreign god. You may:", null, [Events.IgnoreTheirContactWithTheDahan, Events.CurseTheTonguesOfTheForeigners], TokenEvent.PreyOnTheUnwary, null),
        new ChoiceEventCard(ProductSet.BranchAndClaw, "A Strange Madness among the Beasts", "They grow even wilder and more savage. You may:", null, [Events.LetThemRampageUntoDeath, Events.GuideTheMadness], TokenEvent.SavageFrenzy, DahanEvent.SeekASaferHome),
        new StageEventCard(ProductSet.BranchAndClaw, Events.SeekingTheInterior, Events.LocalDiaspora, Events.LocalDiaspora, TokenEvent.BeastsProwl, DahanEvent.ForsakeTheBarrenLand),
        new StageEventCard(ProductSet.BranchAndClaw, Events.WaveOfReconnaissance, Events.Urbanization, Events.Urbanization, TokenEvent.Stricken, DahanEvent.Retreat),
        new StageEventCard(ProductSet.BranchAndClaw, Events.InterestingDiscoveries, Events.IncreasingAggression, Events.IncreasingAggression, TokenEvent.WheezelungOutbreak, DahanEvent.TendTheLand),
        new StageEventCard(ProductSet.BranchAndClaw, Events.StrangeTalesAttractExplorers, Events.Fortification, Events.Fortification, TokenEvent.BeastsAttack, DahanEvent.ComingOfAgeMountainSands),
        new TerrorLevelEventCard(ProductSet.BranchAndClaw, Events.CulturalAssimilation, Events.CulturalAssimilation, Events.ReprisalAgainstTheDahan, TokenEvent.BeastsAttack, DahanEvent.RecklessOffensive),
        new TerrorLevelEventCard(ProductSet.BranchAndClaw, Events.InvestigationOfDangers, Events.DestroyTheUnnatural, Events.DestroyTheUnnatural, TokenEvent.PreyOnTheUnwary, DahanEvent.RouseTheSpirits),
        new TerrorLevelEventCard(ProductSet.BranchAndClaw, Events.DistantExploration, Events.FearfulMobs, Events.FearfulMobs, TokenEvent.GrimToll, DahanEvent.FierceMien),
        new ChoiceEventCard(ProductSet.BranchAndClaw, "Rising Interest in the Island", "Your island is unlike any the Invaders have seen. Their leaders begin to take interest in tales of strangeness. You may:", null, [Events.IgnoreTheCuriosity, Events.WeaveLiesInTheMindsOfTheirObservers], TokenEvent.BeastsOfTheJungle, DahanEvent.TrapsAndSnares),
        new HealthyBlightedLandEventCard(ProductSet.BranchAndClaw, Events.PuttingDownRoots, Events.TheCenterCrumbles, TokenEvent.Stricken, DahanEvent.DriveOffTheInterlopers),
        new HealthyBlightedLandEventCard(ProductSet.BranchAndClaw, Events.SearchForNewLands, Events.DevastatedShores, TokenEvent.DistantHunt, DahanEvent.CannyDefense),
        new HealthyBlightedLandEventCard(ProductSet.BranchAndClaw, Events.InvadersSurgeInland, Events.WideningDestruction, TokenEvent.GrimToll, DahanEvent.CannyDefense),
        new HealthyBlightedLandEventCard(ProductSet.BranchAndClaw, Events.TightKnitCommunities, Events.BlightSpreads, TokenEvent.PreyOnTheUnwary, DahanEvent.ComingOfAgeCoastal),
        new HealthyBlightedLandEventCard(ProductSet.BranchAndClaw, Events.WellPreparedExplorers, Events.BlightSpreads, TokenEvent.BeastsProwl, DahanEvent.ComingOfAgeInland),
        new HealthyBlightedLandEventCard(ProductSet.BranchAndClaw, Events.PopulationRises, Events.PowerFades, TokenEvent.SandfeverOutbreak, DahanEvent.OfferingsOfPatternAndDance),
        new HealthyBlightedLandEventCard(ProductSet.BranchAndClaw, Events.UrbanDevelopment, Events.FesteringPitsOfBlight, TokenEvent.LingeringPlagues, DahanEvent.FierceMien),
        new HealthyBlightedLandEventCard(ProductSet.BranchAndClaw, Events.HeavyFarming, Events.OvercrowdedCities, TokenEvent.PreyOnTheUnwary, DahanEvent.ComingOfAgeJungleWetland),
        new HealthyBlightedLandEventCard(ProductSet.BranchAndClaw, Events.PromisingFarmland, Events.NewCashCropsTakeHold, TokenEvent.BeastsProvoked, DahanEvent.CannyDefense),
        new AdversaryEvent(ProductSet.BranchAndClaw, "Slave Rebellion", Adversary.KingdomOfFrance, new StageEventCard(ProductSet.BranchAndClaw, Events.SmallUprising, Events.SmallUprising, Events.Rebellion, null, DahanEvent.AidTheUprising)),
        // Jagged Earth
        new ChoiceEventCard(ProductSet.JaggedEarth, "Lesser Spirits Imperiled", "The Invaders' spread is threatening many of the island's smaller Spirits. You may:", null, [Events.TendToYourOwnStrength, Events.ForgeAWebOfMutualSupport], TokenEvent.QuitTheFarmedLands, DahanEvent.ReturnToOldPillars),
        new ChoiceEventCard(ProductSet.JaggedEarth, "Remnants of a Spirit's Heart", "A group of Dahan find a stony ridge with lingering blessings from an ancient mountain-Spirit. You may:", null, [Events.LeaveItsStrengthWithTheDahan, Events.WithPatientFocusCraftAGreatWarding], TokenEvent.HuntingParties, DahanEvent.AThousandSmallStruggles),
        new ChoiceEventCard(ProductSet.JaggedEarth, "Numinous Crisis", "The spiritual energy of the island weakens as life's connections grow ever more tattered. You may:", null, [Events.DrawStrengthFromItWhileYouCan, Events.PourYourStrengthIntoTheIsland], TokenEvent.PlaguesBringFearAndDeath, DahanEvent.CarefulDefense),
        new ChoiceEventCard(ProductSet.JaggedEarth, "Hard-Working Settlers", "The latest round of settlers are regrettably diligent, focused and curious. You may:", null, [Events.ActCautiouslyInTheBackground, Events.CreateUnnervingDistractions], TokenEvent.BeastsPreyOnTheInjured, null),
        new ChoiceEventCard(ProductSet.JaggedEarth, "Dahan Trade with the Invaders", "Some seek knowledge, others are interested in tools and trade goods, still others simply curious. All hope to avoid violence, and the Invaders seem amenable - at least for now. You may:", null, [Events.IgnoreTheirInterest, Events.DisplayYourWrathAtThisBetrayal, Events.ChangeAndHelpThemLearnFromTheEnemy], TokenEvent.OutbreaksShift, null),
        new ChoiceEventCard(ProductSet.JaggedEarth, "Life's Balance Tilts", "The energies of life shift towards destruction, bringing wasting and disease to the animals of the island. Death is a part of life, but does this go too far? You may:", null, [Events.LetDestructionHaveItsDay, Events.FortifyTheResilienceOfLife], null, DahanEvent.AThousandSmallStruggles),
        new StageEventCard(ProductSet.JaggedEarth, Events.HarvestBountyHarvestDust, Events.HarvestBountyHarvestDust, Events.WidespreadClearcutting, TokenEvent.ExplorersBlunder, DahanEvent.CoordinatedStrikes),
        new StageEventCard(ProductSet.JaggedEarth, Events.InvestedAristocracy, Events.InvestedAristocracy, Events.ForeignDignitariesVisit, TokenEvent.PreyOnTheHeedlessJE, DahanEvent.ComingOfAge2Dahan),
        new StageEventCard(ProductSet.JaggedEarth, Events.MapmakersChartTheWild, Events.MapmakersChartTheWild, Events.IncreasingAggression, TokenEvent.PreyOnTheHeedlessJE, DahanEvent.ComingOfAgeNoToken),
        new StageEventCard(ProductSet.JaggedEarth, Events.NoBraveryWithoutNumbers, Events.NoBraveryWithoutNumbers, Events.CourageOfTheCrowd, TokenEvent.PreyOnTheHeedlessJE, DahanEvent.LeaveTheHostileLand),
        new StageEventCard(ProductSet.JaggedEarth, Events.SmallerPortsSpringUp, Events.SmallerPortsSpringUp, Events.ExtensiveBuilding, TokenEvent.Stricken, DahanEvent.SettlersEncroachTooFar),
        new HealthyBlightedLandEventCard(ProductSet.JaggedEarth, Events.TheFrontierCalls, Events.SelfSacrificeBuysTime, TokenEvent.LairInUntamedLands, DahanEvent.SeekOutNewGrounds),
        new HealthyBlightedLandEventCard(ProductSet.JaggedEarth, Events.SeekNewFarmland, Events.VoraciousConsumption, TokenEvent.PlaguesBringFearAndDeath, DahanEvent.EngageOnTheirOwnTerms),
        new HealthyBlightedLandEventCard(ProductSet.JaggedEarth, Events.GradualCorruption, Events.RavagedWilderness, TokenEvent.FatalitiesRise, DahanEvent.BlessingsOfBountyAndHealth),
        new HealthyBlightedLandEventCard(ProductSet.JaggedEarth, Events.FortuneSeekers, Events.TheLandsBountyExhausted, TokenEvent.GrimToll, DahanEvent.TellTheOldStories),
        new HealthyBlightedLandEventCard(ProductSet.JaggedEarth, Events.ProvincialSeat, Events.LandsHollowOfPromise, TokenEvent.BeastsChaseOffHomesteaders, DahanEvent.RallyToTheDefenseOfDistantKin),
        new HealthyBlightedLandEventCard(ProductSet.JaggedEarth, Events.CitiesRise, Events.DepletedSoil, TokenEvent.BeastsChaseOffHomesteaders, DahanEvent.CarefulDefense),
        new HealthyBlightedLandEventCard(ProductSet.JaggedEarth, Events.ThrivingTrade, Events.PartitionedWilderness, TokenEvent.PestilenceArrivesOnCanvasSails, DahanEvent.CleverCooperation),
        new HealthyBlightedLandEventCard(ProductSet.JaggedEarth, Events.WoundedLandsAttractExplorers, Events.TheWorldsVibranceFades, TokenEvent.BeastsChaseOffHomesteaders, DahanEvent.RaidingAndRetaliation),
        new HealthyBlightedLandEventCard(ProductSet.JaggedEarth, Events.CoastalTownMultiply, Events.CooperationAmongTowns, TokenEvent.ExplorersBlunder, DahanEvent.ComingOfAgeNoBlightDisease),
        new HealthyBlightedLandEventCard(ProductSet.JaggedEarth, Events.CivicEngagement, Events.LifesWebTornAsunder, TokenEvent.CasualtiesOfFangAndSting, DahanEvent.KeepFarFromTheLandsOfPlague),
        new HealthyBlightedLandEventCard(ProductSet.JaggedEarth, Events.SprawlContainedByTheWilds, Events.DissolutionThreatens, TokenEvent.ExplorersBlunder, DahanEvent.LayAmbushes),
        new HealthyBlightedLandEventCard(ProductSet.JaggedEarth, Events.TheStrugglesOfGrowth, Events.BlightDeepens, TokenEvent.IrregularOutbreaks, DahanEvent.CarefulDefense),
        new TerrorLevelEventCard(ProductSet.JaggedEarth, Events.EagerExplorers, Events.Xenophobia, Events.Xenophobia, TokenEvent.BeastsChaseOffHomesteaders, DahanEvent.AtTheirGatesDemandingRedress),
        new TerrorLevelEventCard(ProductSet.JaggedEarth, Events.BureaucratsAdjustFunding, Events.BureaucratsAdjustFunding, Events.RansackAndRun, TokenEvent.TerrifyingBeasts, DahanEvent.CoordinatedDefense),
        new TerrorLevelEventCard(ProductSet.JaggedEarth, Events.ResourcefulPopulace, Events.StripTheLandBare, Events.StripTheLandBare, TokenEvent.VirulenceAmongClosePackedHomes, DahanEvent.OfferingsOfStoryAndSeason),
        new TerrorLevelEventCard(ProductSet.JaggedEarth, Events.RelentlessOptimism, Events.CulturesMixAndClash, Events.CulturesMixAndClash, TokenEvent.ForeignDiseases, DahanEvent.OfferingsOfPatternAndDance),
        new TerrorLevelEventCard(ProductSet.JaggedEarth, Events.PullTogetherInAdversity, Events.PullTogetherInAdversity, Events.PurgeTheLandWithSaltAndFire, TokenEvent.ExplorersBlunder, DahanEvent.CarefulDefense),
        new TerrorLevelEventCard(ProductSet.JaggedEarth, Events.TemporaryTruce, Events.TemporaryCaution, Events.TemporaryCaution, TokenEvent.PreyOnTheHeedlessJE, DahanEvent.SpeakOfTheSpiritsAnger),
        new TerrorLevelEventCard(ProductSet.JaggedEarth, Events.Overconfidence, Events.TerrorBreedsAggression, Events.TerrorBreedsAggression, TokenEvent.BeastsMultiply, DahanEvent.CoordinatedDefense),
        // Nature Incarnate
        new ChoiceEventCard(ProductSet.NatureIncarnate, "Ethereal Conjunction", "A confluence of spiritual forces gathers into an unformed maelstrom. Each Spirit chooses:", null, [Events.EndureItsForcesAsBestYouCan, Events.SeekToControlItThoughItExhaustsYou], TokenEvent.IrregularOutbreaks, DahanEvent.TendToTheLivingEarth),
        new ChoiceEventCard(ProductSet.NatureIncarnate, "Far-Off Wars Touch the Island", "Invaders from a different, distant land launch an assault upon the island while the invaders here rally together in a wave of nationalism. Defending the island with them might come at too high a price.", ["Add a fear Card to the top of the Fear Deck.", "On Each Board, in the land with the most Town / City, choose (for that board) either:"], [Events.EncourageTheDestruction, Events.BluntTheOffensive], TokenEvent.EcosystemDamage, DahanEvent.ReturnToOldPillars),
        new ChoiceEventCard(ProductSet.NatureIncarnate, "Visions Out of Time", "A Spirit more loosely time-moored than most warns of catastrophe's subtle seeds. Each Spirit chooses:", null, [Events.LetTheWarningWaftIntoDaysPast, Events.HeadOffTheProblemsYourself], TokenEvent.PreyOnTheHeedlessNI, DahanEvent.StrengthFromTrade),
        new HealthyBlightedLandEventCard(ProductSet.NatureIncarnate, Events.AccumulatedDevastation, Events.TheWorldsVibranceFades, TokenEvent.TerritorialBeasts, DahanEvent.YearsOfHealthAndHarmony),
        new HealthyBlightedLandEventCard(ProductSet.NatureIncarnate, Events.FocusedFarming, Events.EssenceDisperses, TokenEvent.ExplorersBlunder, DahanEvent.OfferingsOfStoryAndSeason),
        new HealthyBlightedLandEventCard(ProductSet.NatureIncarnate, Events.InfluxOfSettlers, Events.LethargyAndDegeneration, TokenEvent.SandStalkers, DahanEvent.NetworkOfSupportAndTrade),
        new HealthyBlightedLandEventCard(ProductSet.NatureIncarnate, Events.SearchForUnclaimedLand, Events.WidespreadHunting, TokenEvent.PlaguesInPopulousLands, DahanEvent.SpreadingConflictPromptsCaution),
        new TerrorLevelEventCard(ProductSet.NatureIncarnate, Events.AnOminousDawn, Events.WaveringResolve, Events.WaveringResolve, TokenEvent.DangerousLands, DahanEvent.WaningSupport),
        new TerrorLevelEventCard(ProductSet.NatureIncarnate, Events.TerrorSpikesUpwards, Events.TerrorSpikesUpwards, Events.FinalHarvest, TokenEvent.SecureSettledTerritory, DahanEvent.WarAmongTheDahan),
        // Blight
        // Basegame
        new BlightCard(ProductSet.Basegame, BlightType.BlightedIsland, "Downward Spiral", 5, "At the start of each Invader Phase each Spirit destroys 1 of their Presence."),
        new BlightCard(ProductSet.Basegame, BlightType.BlightedIsland, "Memory Fades to Dust", 4, "At the start of each Invader Phase each Spirit Forgets a Power or destroys 1 of their Presence."),
        // Branch & Claw
        new BlightCard(ProductSet.BranchAndClaw, BlightType.BlightedIsland, "Back Against the Wall", 2, "Every Spirit Phase each Spirit gains +1 Energy and +1 Card Play."),
        new BlightCard(ProductSet.BranchAndClaw, BlightType.BlightedIsland, "Promising Farmlands", 4, "Immediately, on each board: Add 1 Town and 1 City to an Inland land with no Town / City."),
        new BlightCard(ProductSet.BranchAndClaw, BlightType.BlightedIsland, "Disintegrating Ecosystem", 5, "Immediately, on each board: Destroy 1 Beasts, then add 1Blight to a land with Town / City."),
        new BlightCard(ProductSet.BranchAndClaw, BlightType.BlightedIsland, "Aid from Lesser Spirits", 2, "Immediately, draw 1 Minor Power Card per player plus 1 more. Give 1 to each Spirit. They may be used every turn as if played, but cost no Card Plays / Energy. Place unselected card in Minor Powers discard pile."),
        new BlightCard(ProductSet.BranchAndClaw, BlightType.BlightedIsland, "Tipping Point", 5, "Immediately, destroy 3 resence from each Spirit."),
        new BlightCard(ProductSet.BranchAndClaw, BlightType.BlightedIsland, "Erosion of Will", 3, "Immediately, 2 Fear per player. Each Spirit destroys 1 of their Presence and loses 1 Energy."),
        new BlightCard(ProductSet.BranchAndClaw, BlightType.BlightedIsland, "A Pall upon the Land", 3, "Immediately, on each board: destroy 1 Presence and remove 1 Town."),
        // Jagged Earth
        new BlightCard(ProductSet.JaggedEarth, BlightType.BlightedIsland, "Unnatural Proliferation", 3, "Immediately: Each Spirit adds 1 Presence to a land with their Presence. On Each Board: Add 1 Dahan to a land with Dahan, and 2 City to the land with fewest Town / City (min. 1)."),
        new BlightCard(ProductSet.JaggedEarth, BlightType.BlightedIsland, "All Things Weaken", 3, "Ongoing, starting next turn: Invaders and Dahan have -1 Health (min. 1). The land takes Blight on 1 less Damage (normally 1). When you add Blight, it Destroys all Presence / Beasts in that land and 1 Presence (total) in an adjacent land."),
        new BlightCard(ProductSet.JaggedEarth, BlightType.BlightedIsland, "Thriving Communities", 4, "Immediately, on each board: In 4 different lands with Explorer / Town, Replace 1 Town with1 City or Replace 1 Explorer with 1 Town."),
        new BlightCard(ProductSet.JaggedEarth, BlightType.BlightedIsland, "Power Corrodes the Spirit", 4, "At the start of each Invader Phase each Spirit Destroys 1 of their Presence if they have 3 or more Power Cards in play, or have a Power Card in play costing 4 or more (printed) Energy."),
        new BlightCard(ProductSet.JaggedEarth, BlightType.BlightedIsland, "Untended Land Crumbles", 4, "At the start of each Invader Phase, On Each Board: Add 1 Blight to a land adjacent to Blight. Spirits may prevent this on any / all boards; each board to be protected requires jointly paying 3 Energy or Destroying 1 Presence from that board."),
        new BlightCard(ProductSet.JaggedEarth, BlightType.StillHealthyIsland, "Invaders find the Land to their Liking", 2, "Immediately: If the Terror Level is I / II / III, add 1 / 1.5 / 2 Fear Markers per player to the Fear pool. (Round down at Terror Level II.)"),
        new BlightCard(ProductSet.JaggedEarth, BlightType.StillHealthyIsland, "Strong Earth Shatters Slowly", 2, "Immediately: Each player adds 1 Blight (from this card) to a land adjacent to Blight."),
        // Nature Incarnate
        new BlightCard(ProductSet.NatureIncarnate, BlightType.BlightedIsland, "Attenuated Essence", 4, "Each Invader Phase: Each Spirit with at least 5 Presence on the island Destroys 1 Presence."),
        new BlightCard(ProductSet.NatureIncarnate, BlightType.BlightedIsland, "Blight Corrodes the Spirit", 4, "Each Invader Phase: On Each Board, Destroy 1 Presence in a land with Blight."),
        new BlightCard(ProductSet.NatureIncarnate, BlightType.BlightedIsland, "Burn Brightest Before the End", 2, "Immediately: Each Spirit Adds 1 Presence to one of their lands or removes 1 Presence from their Presence Tracks. (Presence removed from Presence Tracks goes to the Destroyed Presence supply.)"),
        new BlightCard(ProductSet.NatureIncarnate, BlightType.BlightedIsland, "Intensifying Exploitation", 5, "Ongoing, starting next turn: During Ravage Actions, Invaders deal +2 Damage (per land)."),
        new BlightCard(ProductSet.NatureIncarnate, BlightType.BlightedIsland, "Shattered Fragments of Power", 2, "Immediately: Draw 1 Major Power Card per Spirit plus 2 more. Each Spirit Takes 1 and gains 2 Energy. (Discard the 2 unselected cards.)"),
        new BlightCard(ProductSet.NatureIncarnate, BlightType.BlightedIsland, "Slow Dissolution of Will", 3, "Immediately: Each Spirit chooses one of Badlands, Beasts or Wilds. (Put some of the chose Tokens next to your Spirit Panel as a reminder.) Each Invader Phase: Each Spirit Replaces 1 Presence with their chosen type of Spirit Token. (The Presence goes to the Destroyed Presence supply.)"),
        new BlightCard(ProductSet.NatureIncarnate, BlightType.StillHealthyIsland, "The Border of Life and Death", 1, "Now and Each Invader Phase (until this card is replaced): Each Spirit with at least 2 Presence on the island Destroys 1 Presence and may discard a Power Card to gain 1 Energy."),
        new BlightCard(ProductSet.NatureIncarnate, BlightType.StillHealthyIsland, "Thriving Crops", 2, "Immediately: On Each Board, Build in 3 lands. (Build Actions in lands without Invaders normally Build 1 Town.)"),
    ];
})(DB || (DB = {}));
/// <reference path="types.ts">
/// <reference path="parser.ts">
var Filter;
(function (Filter_1) {
    var Compiled;
    (function (Compiled) {
        function compile(ast) {
            const test = compileToString(ast);
            console.log(test);
            const fn = new Function("cards", "return cards.filter(card => " + test + ");");
            return fn;
        }
        Compiled.compile = compile;
        function compileToString(f) {
            switch (f.kind) {
                case "text": return "card.getSearchString().includes(\"" + escapeString(f.text) + "\")";
                case "regex": return "card.getSearchString().search(" + (f.regex == "" ? "new RegExp()" : "/" + f.regex + "/") + ") != -1";
                case "propfilter":
                    switch (f.filter.kind) {
                        case "numfilter": return "((prop = card[\"" + escapeString(f.property) + "\"]) == null ? false : prop " + Lexer.comparisonTypeToString(f.filter.typ) + " " + f.filter.number + ")";
                        case "text":
                            return "(" +
                                "(prop = card[\"" + escapeString(f.property) + "\"]) == null ? false : (" +
                                "(prop = (prop == Types.LandAny ? 'Any' : prop.toString().replace(/&/g, 'and')).toLowerCase()).includes(" +
                                "\"" + escapeString(f.filter.text) + "\"" +
                                ")" +
                                ")" +
                                ")";
                        case "regex":
                            return "(" +
                                "(prop = card[\"" + escapeString(f.property) + "\"]) == null ? false : (" +
                                "(prop = (prop == Types.LandAny ? 'Any' : prop.toString().replace(/&/g, 'and')).toLowerCase()).search(" +
                                (f.filter.regex == "" ? "new RegExp()" : "/" + f.filter.regex + "/") +
                                ") != -1" +
                                ")" +
                                ")";
                        default: assertNever(f.filter);
                    }
                    throw new Error("unreachable");
                case "not": return "!" + compileToString(f.filter);
                case "and": return "(" + compileToString(f.a) + " && " + compileToString(f.b) + ")";
                case "or": return "(" + compileToString(f.a) + " || " + compileToString(f.b) + ")";
                default: assertNever(f);
            }
        }
        function escapeString(s) {
            return s.replace(/"/g, "\\\"");
        }
        function assertNever(x) {
            throw new Error("Unexpected Object: " + x);
        }
    })(Compiled = Filter_1.Compiled || (Filter_1.Compiled = {}));
})(Filter || (Filter = {}));
/// <reference path="types.ts" />
var Filter;
(function (Filter_2) {
    var Old;
    (function (Old) {
        class ExtensibleFunction extends Function {
            constructor(fn) {
                super();
                return Object.setPrototypeOf(fn, new.target.prototype);
            }
        }
        class Filter extends ExtensibleFunction {
            constructor(fn) {
                let fnString = fn.toString();
                super(fn);
                this.fnString = fnString;
            }
            static all(...filters) {
                return new Filter((card) => filters.reduce((res, filter) => res && filter(card), true));
            }
            toString() {
                return "Filter: " + this.fnString;
            }
        }
        class NegationFilter extends Filter {
            constructor(filter) {
                super((card) => !filter(card));
            }
        }
        class PropFilter extends Filter {
            constructor(property, f) {
                super((card) => {
                    let val = card[this.property];
                    if (val == null) {
                        return false;
                    }
                    return this.f(val);
                });
                this.property = property;
                this.f = f;
            }
            toString() {
                return "PropFilter on " + this.property + ": " + this.f.toString();
            }
        }
        class IncludesFilter extends Filter {
            constructor(includes) {
                super((card) => {
                    const cardstring = card.getSearchString().toLowerCase();
                    return cardstring.includes(includes);
                });
                this.includes = includes;
            }
            toString() {
                return "IncludesFilter should include '" + this.includes + "'";
            }
        }
        class PropIncludesFilter extends PropFilter {
            constructor(prop, includes) {
                super(prop, (val) => {
                    const propstring = propToString(val).toLowerCase();
                    return propstring.includes(this.includes);
                });
                this.prop = prop;
                this.includes = includes;
            }
            toString() {
                return "PropIncludesFilter on " + this.prop + " should include '" + this.includes + "'";
            }
        }
        class PropWholeWordFilter extends PropFilter {
            constructor(prop, word) {
                super(prop, (val) => {
                    const propstring = propToString(val).toLowerCase();
                    return this.regex.test(propstring);
                });
                this.prop = prop;
                this.word = word;
                let escaped = regexEscape(this.word);
                let delim = "(^|$|[^a-zA-Z0-9_])";
                let regex = delim + escaped + delim;
                this.regex = new RegExp(regex);
            }
            toString() {
                return "PropWholeWordFilter on " + this.prop + " should include word group '" + this.word
                    + "' by testing for " + this.regex;
            }
        }
        class WholeWordFilter extends Filter {
            constructor(word) {
                super((card) => {
                    const cardstring = card.getSearchString().toLowerCase();
                    return this.regex.test(cardstring);
                });
                this.word = word;
                let escaped = regexEscape(this.word);
                let delim = "(^|$|[^a-zA-Z0-9_])";
                let regex = delim + escaped + delim;
                this.regex = new RegExp(regex);
            }
            toString() {
                return "WholeWordFilter should include word group '" + this.word + "' by testing for " + this.regex;
            }
        }
        function regexEscape(str) {
            return str.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
        }
        function getPropertyFilterString(search, name) {
            let idx = search.indexOf(name + ":");
            if (idx >= 0) {
                let start = idx + name.length + 1;
                let end;
                if (search[start] == '"' || (search[start] == "!" && search.length > start + 1 && search[start + 1] == '"')) {
                    end = search.indexOf('"', search[start] == "!" ? start + 2 : start + 1);
                    end = end == -1 ? search.length : end + 1;
                }
                else {
                    end = search.indexOf(' ', start);
                    end = end == -1 ? search.length : end;
                }
                return [search.substring(start, end), search.substring(0, idx) + search.substring(end + 1, search.length), idx];
            }
            return [null, search, null];
        }
        function propToString(prop) {
            if (prop == LandAny) {
                return "Any";
            }
            return prop.toString().replace(/&/g, "and");
        }
        function stringToPropertyFilter(filterString, property) {
            if (filterString.startsWith("<=")) {
                return new PropFilter(property, (val) => val <= filterString.substring(2));
            }
            else if (filterString.startsWith(">=")) {
                return new PropFilter(property, (val) => val >= filterString.substring(2));
            }
            else if (filterString.startsWith("<")) {
                return new PropFilter(property, (val) => val < filterString.substring(1));
            }
            else if (filterString.startsWith(">")) {
                return new PropFilter(property, (val) => val > filterString.substring(1));
            }
            else if (filterString.startsWith("!")) {
                return new NegationFilter(stringToPropertyFilter(filterString.substring(1), property));
            }
            else if (filterString.startsWith('"')) {
                let end;
                if (filterString.endsWith('"') && filterString.length > 1) {
                    end = filterString.length - 1;
                }
                else {
                    end = filterString.length;
                }
                return new PropWholeWordFilter(property, filterString.substring(1, end));
            }
            else {
                return new PropIncludesFilter(property, filterString);
            }
        }
        function getPropertyFilters(searchstring, property) {
            let filter = "";
            let search = searchstring;
            let filters = [];
            while (filter != null) {
                [filter, search] = getPropertyFilterString(search, property);
                if (filter == null) {
                    break;
                }
                filters.push(stringToPropertyFilter(filter, property));
            }
            return [filters, search];
        }
        function getAllFilters(searchstring) {
            let filters = [];
            // property filters
            const props = Types.getCardProperties();
            for (const prop of props) {
                let fs;
                [fs, searchstring] = getPropertyFilters(searchstring, prop);
                filters = filters.concat(fs);
            }
            // word groups
            let groups = searchgroups(searchstring);
            for (const group of groups) {
                if (group.startsWith('"')) {
                    let end;
                    if (group.endsWith('"')) {
                        end = group.length - 1;
                    }
                    else {
                        end = group.length;
                    }
                    filters.push(new WholeWordFilter(group.substring(1, end)));
                }
                else {
                    filters.push(new IncludesFilter(group));
                }
            }
            return filters;
        }
        function filterAll(cards, searchstring) {
            searchstring = searchstring.replace(/&/g, "and");
            const filters = getAllFilters(searchstring);
            cards = cards.filter(c => Filter.all(...filters)(c));
            return cards;
        }
        Old.filterAll = filterAll;
        function searchgroups(search) {
            let res = [];
            if (search.length == 0) {
                return res;
            }
            while (search.indexOf('"') >= 0) {
                let start = search.indexOf('"');
                let end = search.indexOf('"', start + 1) + 1;
                if (end == 0) {
                    end = search.length;
                }
                res.push(search.substring(start, end));
                search = search.substring(0, start) + search.substring(end);
            }
            res = res.concat(search.split(" "));
            return res;
        }
    })(Old = Filter_2.Old || (Filter_2.Old = {}));
})(Filter || (Filter = {}));
/// <reference path="types.ts">
/// <reference path="parser.ts">
/// <reference path="filter-old.ts">
/// <reference path="filter-compiled.ts">
var Filter;
(function (Filter) {
    let FilterType;
    (function (FilterType) {
        FilterType[FilterType["Old"] = 0] = "Old";
        FilterType[FilterType["Compiled"] = 1] = "Compiled";
    })(FilterType = Filter.FilterType || (Filter.FilterType = {}));
    function filterAll(cards, searchstring, typ) {
        searchstring = searchstring.replace(/&/g, "and");
        switch (typ) {
            case FilterType.Old: return Filter.Old.filterAll(cards, searchstring);
            case FilterType.Compiled:
                const ast = Parser.parseFilters(searchstring);
                if (ast == null) {
                    return cards;
                }
                const fn = Filter.Compiled.compile(ast);
                return fn(cards);
        }
    }
    Filter.filterAll = filterAll;
})(Filter || (Filter = {}));
var Lexer;
(function (Lexer) {
    let ComparisonType;
    (function (ComparisonType) {
        ComparisonType[ComparisonType["LessThan"] = 0] = "LessThan";
        ComparisonType[ComparisonType["LessEquals"] = 1] = "LessEquals";
        ComparisonType[ComparisonType["Equals"] = 2] = "Equals";
        ComparisonType[ComparisonType["GreaterEquals"] = 3] = "GreaterEquals";
        ComparisonType[ComparisonType["GreaterThan"] = 4] = "GreaterThan";
    })(ComparisonType = Lexer.ComparisonType || (Lexer.ComparisonType = {}));
    function comparisonTypeToString(c) {
        switch (c) {
            case ComparisonType.LessThan: return "<";
            case ComparisonType.LessEquals: return "<=";
            case ComparisonType.Equals: return "==";
            case ComparisonType.GreaterEquals: return ">=";
            case ComparisonType.GreaterThan: return ">";
        }
    }
    Lexer.comparisonTypeToString = comparisonTypeToString;
    function lex(s) {
        const tokens = [];
        let index = 0;
        while (!eof(index, s)) {
            let token;
            ({ index, result: token } = lexToken(index, s));
            tokens.push(token);
        }
        return tokens;
    }
    Lexer.lex = lex;
    function lexToken(index, s) {
        switch (true) {
            case s[index] == '"': return lexDoubleQuotedString(index, s);
            case s[index] == '!': return { index: index + 1, result: { kind: "bang", span: [index, index + 1] } };
            case s[index] == ':': return { index: index + 1, result: { kind: "colon", span: [index, index + 1] } };
            case s[index] == ',': return { index: index + 1, result: { kind: "comma", span: [index, index + 1] } };
            case s[index] == "|": return { index: index + 1, result: { kind: "pipe", span: [index, index + 1] } };
            case s[index] == "(": return { index: index + 1, result: { kind: "openparen", span: [index, index + 1] } };
            case s[index] == ")": return { index: index + 1, result: { kind: "closeparen", span: [index, index + 1] } };
            case s[index] == "/":
                const regex = lexRegex(index, s);
                if (regex == null) {
                    return lexWord(index, s);
                }
                else {
                    return regex;
                }
            case /\s/.test(s[index]): return lexWhitespace(index, s);
            case /\d/.test(s[index]): return lexInteger(index, s);
            case /[<=>]/.test(s[index]): return lexComparison(index, s);
            default: return lexWord(index, s);
        }
    }
    function lexRegex(index, s) {
        if (s[index] != "/") {
            throw new Error("lexRegExp called without leading slash character");
        }
        const start = index;
        index += 1;
        while (!eof(index, s) && s[index] != "/") {
            ({ index } = consumePossiblyEscapedChar(index, s));
        }
        // While dqstrings could not be closed yet, we should accept plain slashes as text
        if (s[index] != "/") {
            return null;
        }
        index++;
        return { index, result: { kind: "regex", span: [start, index], regex: s.substring(start + 1, index - 1) } };
    }
    function lexDoubleQuotedString(index, s) {
        if (s[index] != '"') {
            throw new Error("lexDoubleQuotedString called without leading double-quote character");
        }
        const dqStringStart = index;
        index += 1;
        const textStart = index;
        while (!eof(index, s) && s[index] != '"') {
            ({ index } = consumePossiblyEscapedChar(index, s));
        }
        const textEnd = index;
        index += 1;
        const dqStringEnd = index;
        return { index, result: { kind: "dqstring", span: [dqStringStart, dqStringEnd], text: s.substring(textStart, textEnd) } };
    }
    function consumePossiblyEscapedChar(index, s) {
        if (s[index] == "\\") {
            if (eof(index + 1, s)) {
                return { index: index + 1, result: undefined };
            }
            return { index: index + 2, result: undefined };
        }
        else {
            return { index: index + 1, result: undefined };
        }
    }
    function lexWord(index, s) {
        const startIndex = index;
        let word;
        ({ index, result: word } = matchRegex(index, s, /[^:,|()\s]/));
        return { index, result: { kind: "word", span: [startIndex, index], text: word } };
    }
    /** Parses a number comparison operator (must consume at least one character) **/
    function lexComparison(index, s) {
        if (s[index] == '<') {
            if (!eof(index + 1, s) && s[index + 1] == '=') {
                return { index: index + 2, result: { kind: "comparison", span: [index, index + 2], typ: ComparisonType.LessEquals } };
            }
            return { index: index + 1, result: { kind: "comparison", span: [index, index + 1], typ: ComparisonType.LessThan } };
        }
        else if (s[index] == '=') {
            return { index: index + 1, result: { kind: "comparison", span: [index, index + 1], typ: ComparisonType.Equals } };
        }
        else if (s[index] == '>') {
            if (!eof(index + 1, s) && s[index + 1] == '=') {
                return { index: index + 2, result: { kind: "comparison", span: [index, index + 2], typ: ComparisonType.GreaterEquals } };
            }
            return { index: index + 1, result: { kind: "comparison", span: [index, index + 1], typ: ComparisonType.GreaterThan } };
        }
        else {
            throw new Error("lexComparison called without a comparison operator");
        }
    }
    /** Parses an integer number. Must consume at least one character. **/
    function lexInteger(index, s) {
        const startIndex = index;
        const res = matchRegex(index, s, /\d/);
        const { index: newIndex, result: word } = res;
        const number = parseInt(word);
        return { index: newIndex, result: { kind: "int", span: [startIndex, newIndex], number } };
    }
    /** Consumes as much whitespace as possible (must consume at least one) **/
    function lexWhitespace(index, s) {
        const startIndex = index;
        const res = matchRegex(index, s, /\s/);
        let ws;
        ({ index, result: ws } = res);
        if (ws.length == 0) {
            throw new Error("lexWhitespace called without whitespace");
        }
        return { index, result: { kind: "whitespace", span: [startIndex, index] } };
    }
    /** Matches the given regex as often as possible from the given index in the string, returning the whole match. **/
    function matchRegex(index, s, regex) {
        let consumed = 0;
        while (regex.test(s[index])) {
            index += 1;
            consumed += 1;
            if (eof(index, s)) {
                break;
            }
        }
        return { index, result: s.substring(index - consumed, index) };
    }
    function eof(index, s) {
        return index >= s.length;
    }
})(Lexer || (Lexer = {}));
/// <reference path="db.ts" />
/// <reference path="types.ts" />
/// <reference path="filter.ts" />
var FilterType = Filter.FilterType;
const LandAny = Types.LandAny;
const Card = Types.Card;
const CARDS = DB.CARDS;
const EXTRA_CARDS = [];
// https://www.poftut.com/get-query-string-url-javascript/
function getParameterByName(name) {
    let url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    let regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"), results = regex.exec(url);
    if (!results)
        return null;
    if (!results[2])
        return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}
// https://stackoverflow.com/a/3540295
var isMobile = false;
if (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent)
    || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0, 4))) {
    isMobile = true;
}
const updateTime = isMobile ? 1000 : 300;
document.addEventListener("DOMContentLoaded", () => {
    const body = document.getElementsByTagName("body")[0];
    const search = document.getElementById("search");
    const sort = document.getElementById("sort");
    const order = document.getElementById("arrow");
    for (let i = 0; i < 10; i++) {
        let flex = document.createElement("div");
        flex.classList.add("flex-50", "xs-flex-33", "sm-flex-25", "md-flex-20", "l-flex-15", "xl-flex-12", "xxl-flex-10");
        flex.style.height = "0px";
        EXTRA_CARDS.push(flex);
    }
    body.onresize = () => CARDS.forEach(c => c.onresize());
    body.onkeypress = e => {
        if (e.key === 's' && !(e.target instanceof HTMLInputElement)) {
            search.focus();
            e.preventDefault();
        }
    };
    let timeout;
    search.oninput = _ => {
        clearTimeout(timeout);
        timeout = setTimeout(() => update(), updateTime);
    };
    search.onblur = _ => {
        clearTimeout(timeout);
        update();
    };
    sort.onchange = _ => {
        clearTimeout(timeout);
        update();
    };
    order.onclick = _ => {
        clearTimeout(timeout);
        order.classList.toggle("rotated");
        update();
    };
    // get query parameter
    let query = getParameterByName("query");
    if (query) {
        search.value = query;
    }
    update();
});
function update() {
    const search = document.getElementById("search");
    const result = document.getElementById("result");
    const numResults = document.getElementById("num-results");
    const sort = document.getElementById("sort");
    const order = document.getElementById("arrow");
    history.replaceState(null, "", "?query=" + encodeURIComponent(search.value));
    // clear old content
    while (result.firstChild) {
        result.removeChild(result.firstChild);
    }
    let searchstring = search.value.toLowerCase().replace(/&/g, "and");
    let sortby = sort.value.toLowerCase();
    let ascending = !order.classList.contains("rotated");
    let cards = CARDS;
    cards = Filter.filterAll(cards, searchstring, FilterType.Compiled);
    numResults.innerText = "Results: " + cards.length;
    cards = cards.sort((a, b) => {
        let propa = a[sortby];
        let propb = b[sortby];
        if (propa === undefined) {
            return 1;
        }
        if (propb === undefined) {
            return -1;
        }
        let st = ascending ? -1 : 1;
        let gt = ascending ? 1 : -1;
        return propa === propb ? 0 : (propa < propb ? st : gt);
    });
    for (const card of cards) {
        result.appendChild(card.getCardFlexElement());
    }
    // add a few extra to make sure that the trailing line is full as well
    for (let flex of EXTRA_CARDS) {
        result.appendChild(flex);
    }
}
/// <reference path="lexer.ts" />
/// <reference path="types.ts" />
var Parser;
(function (Parser) {
    // Syntax:
    //                 filters : filter ((' ' | ',' | '|') filter)*
    //                  filter : prop_filter | text | not_filter | paren_filter
    //            paren_filter : '(' filters ')'
    //              not_filter : '!' filter
    //             prop_filter : word ':' prop_filter_value_list
    //  prop_filter_value_list : prop_filter_value ((',' | '|') prop_filter_value)* // no spaces anywhere
    //       prop_filter_value : num_filter | text
    // prop_filter_paren_value : '(' prop_filter_value_list ')'
    //   prop_filter_not_value : '!' prop_filter_value
    //              num_filter : ('<' | '<=' | '=' | '>=' | '>')? number
    //                    text : word | dqstring
    //                    word : [a-zA-Z0-9<=>]*
    //                dqstring : // double quoted string possibly with escaped quotes
    //                  number : [0-9]*
    var ComparisonType = Lexer.ComparisonType;
    var comparisonTypeToString = Lexer.comparisonTypeToString;
    let BinOpPrecedence;
    (function (BinOpPrecedence) {
        // lowest = least precedence
        BinOpPrecedence[BinOpPrecedence["Lowest"] = 0] = "Lowest";
        BinOpPrecedence[BinOpPrecedence["Paren"] = 1] = "Paren";
        BinOpPrecedence[BinOpPrecedence["Or"] = 2] = "Or";
        BinOpPrecedence[BinOpPrecedence["And"] = 3] = "And";
        BinOpPrecedence[BinOpPrecedence["Highest"] = 4] = "Highest";
    })(BinOpPrecedence || (BinOpPrecedence = {}));
    function toString(f) {
        switch (f.kind) {
            case "text": return '"' + f.text + '"';
            case "regex": return "/" + f.regex + "/";
            case "not": return "!" + toString(f.filter);
            case "propfilter": return f.property + ":" + propFilterToString(f.filter);
            case "and": return "(" + toString(f.a) + " AND " + toString(f.b) + ")";
            case "or": return "(" + toString(f.a) + " OR " + toString(f.b) + ")";
            default: assertNever(f);
        }
    }
    Parser.toString = toString;
    function propFilterToString(f) {
        switch (f.kind) {
            case "text": return '"' + f.text + '"';
            case "regex": return "/" + f.regex + "/";
            case "numfilter": return comparisonTypeToString(f.typ) + f.number;
            default: assertNever(f);
        }
    }
    function parseFilters(s) {
        const tokens = Lexer.lex(s);
        const filterRes = parseFiltersWithPrecedence(BinOpPrecedence.Lowest, 0, tokens);
        if (filterRes == null) {
            return null;
        }
        const { result: filter } = filterRes;
        return filter;
    }
    Parser.parseFilters = parseFilters;
    function parseFiltersWithPrecedence(currentPrecedence, index, tokens) {
        const wsResult = consumeWhitespace(index, tokens);
        if (wsResult == null) {
            return null;
        }
        ({ index } = wsResult);
        if (eof(index, tokens)) {
            return null;
        }
        const not = tokens[index].kind == "bang";
        if (not) {
            index++;
            if (eof(index, tokens)) {
                return null;
            }
        }
        let lhs;
        let token = tokens[index];
        switch (token.kind) {
            case "openparen":
                const filterRes = parseFiltersWithPrecedence(BinOpPrecedence.Paren, index + 1, tokens);
                if (filterRes == null) {
                    return null;
                }
                ({ index, result: lhs } = filterRes);
                if (eof(index, tokens)) {
                    return null;
                }
                if (tokens[index].kind != "closeparen") {
                    console.error("Unclosed parenthesis at " + token.span[0]);
                }
                else {
                    index++;
                }
                break;
            case "closeparen":
                // if we are somewhere within the parse tree, the closing paren could be handled by an upper recursion instance
                if (currentPrecedence == BinOpPrecedence.Lowest) {
                    console.error("Unmatched close parenthesis in filter list at " + token.span[0]);
                }
                return null;
            default:
                const filterResult = parseFilter(index, tokens);
                if (filterResult == null) {
                    return null;
                }
                ({ index, result: lhs } = filterResult);
        }
        if (not) {
            lhs = { kind: "not", filter: lhs };
        }
        while (true) {
            let rhs;
            // test for following binops
            if (eof(index, tokens)) {
                return { index, result: lhs };
            }
            const binOpToken = tokens[index];
            switch (binOpToken.kind) {
                case "whitespace":
                    const ws2Result = consumeWhitespace(index, tokens);
                    if (ws2Result == null) {
                        throw new Error("this literally can't happen");
                    }
                    ({ index } = ws2Result);
                    const wsRhsResult = parseFiltersWithPrecedence(BinOpPrecedence.And, index, tokens);
                    if (wsRhsResult == null) {
                        // a different operator is following (or there is a syntax error), continue loop
                        continue;
                    }
                    // we actually got whitespace as an AND, check precedence level
                    if (currentPrecedence > BinOpPrecedence.And) {
                        return { index, result: lhs };
                    }
                    ({ index, result: rhs } = wsRhsResult);
                    lhs = { kind: "and", a: lhs, b: rhs };
                    continue;
                // binary operators
                case "comma":
                    if (currentPrecedence > BinOpPrecedence.And) {
                        return { index, result: lhs };
                    }
                    const andRhsResult = parseFiltersWithPrecedence(BinOpPrecedence.And, index + 1, tokens);
                    if (andRhsResult == null) {
                        // whitespace could follow, indicating the comma was for filter-and and not prop-filter-value-and
                        return { index, result: lhs };
                    }
                    ({ index, result: rhs } = andRhsResult);
                    lhs = { kind: "and", a: lhs, b: rhs };
                    continue;
                case "pipe":
                    if (currentPrecedence > BinOpPrecedence.Or) {
                        return { index, result: lhs };
                    }
                    const orRhsResult = parseFiltersWithPrecedence(BinOpPrecedence.Or, index + 1, tokens);
                    if (orRhsResult == null) {
                        return { index, result: lhs };
                    }
                    ({ index, result: rhs } = orRhsResult);
                    lhs = { kind: "or", a: lhs, b: rhs };
                    continue;
                case "closeparen":
                    // if we are somewhere within the parse tree, the closing paren could be handled by an upper recursion instance
                    if (currentPrecedence == BinOpPrecedence.Lowest) {
                        console.error("Unmatched close parenthesis in filter list at " + token.span[0]);
                    }
                    return { index, result: lhs };
                // invalid tokens
                case "openparen":
                case "int":
                case "comparison":
                case "word":
                case "dqstring":
                case "bang":
                case "colon":
                case "regex":
                    console.error("invalid token '" + binOpToken.kind + "' at " + binOpToken.span[0]);
                    return { index, result: lhs };
                default: assertNever(binOpToken);
            }
        }
    }
    function parseFilter(index, tokens) {
        const wsRes = consumeWhitespace(index, tokens);
        if (wsRes == null) {
            return null;
        }
        const propRes = parsePropertyFilter(index, tokens);
        if (propRes != null) {
            return propRes;
        }
        const textResult = parseText(index, tokens);
        if (textResult != null) {
            let { index: newIndex, result: text } = textResult;
            return { index: newIndex, result: { kind: "text", text } };
        }
        const regexResult = parseRegex(index, tokens);
        if (regexResult == null) {
            return null;
        }
        let { index: newIndex, result: regex } = regexResult;
        return { index: newIndex, result: { kind: "regex", regex } };
    }
    function parsePropertyFilter(index, tokens) {
        const res = applyParseFunction(index, tokens, parseWord, consumeWhitespace, checkTokenKind.bind(null, "colon"), consumeWhitespace, parsePropertyFilterValueList.bind(null, BinOpPrecedence.Lowest));
        if (res == null) {
            return null;
        }
        const { index: newIndex, result: [property, /*ws*/ , /*:*/ , /*ws*/ , valueFilterList] } = res;
        const cardProperties = Types.getCardProperties();
        if (cardProperties.indexOf(property) == -1) {
            console.error("Unknown card property '" + property + "'\n" + "Allowed properties are: " + cardProperties);
            // continue
        }
        index = newIndex;
        function convertPropertyFilter(property, filter) {
            switch (filter.kind) {
                case "numfilter":
                    return { kind: "propfilter", property, filter };
                case "text":
                    return { kind: "propfilter", property, filter };
                case "regex":
                    return { kind: "propfilter", property, filter };
                case "propand":
                    return { kind: "and", a: convertPropertyFilter(property, filter.a), b: convertPropertyFilter(property, filter.b) };
                case "propor":
                    return { kind: "or", a: convertPropertyFilter(property, filter.a), b: convertPropertyFilter(property, filter.b) };
                case "propnot":
                    return { kind: "not", filter: convertPropertyFilter(property, filter.filter) };
                default: assertNever(filter);
            }
        }
        return { index, result: convertPropertyFilter(property, valueFilterList) };
    }
    function parsePropertyFilterValueList(currentPrecedence, index, tokens) {
        let lhs;
        if (eof(index, tokens)) {
            return null;
        }
        const not = tokens[index].kind == "bang";
        if (not) {
            index++;
            if (eof(index, tokens)) {
                return null;
            }
        }
        const token = tokens[index];
        switch (token.kind) {
            case "openparen":
                const filterRes = parsePropertyFilterValueList(BinOpPrecedence.Paren, index + 1, tokens);
                if (filterRes == null) {
                    return null;
                }
                ({ index, result: lhs } = filterRes);
                if (eof(index, tokens)) {
                    return null;
                }
                if (tokens[index].kind != "closeparen") {
                    console.error("Unclosed parenthesis at " + token.span[0]);
                }
                else {
                    index++;
                }
                break;
            case "closeparen":
                // if we are somewhere within the parse tree, the closing paren could be handled by an upper recursion instance
                if (currentPrecedence == BinOpPrecedence.Lowest) {
                    console.error("Unmatched close parenthesis in property value list at " + token.span[0]);
                }
                return null;
            default:
                const valueRes = parsePropertyFilterValue(index, tokens);
                if (valueRes == null) {
                    return null;
                }
                ({ index, result: lhs } = valueRes);
        }
        if (not) {
            lhs = { kind: "propnot", filter: lhs };
        }
        // parse and merge while same precedence until higher precedence
        while (true) {
            // peek for operators with same or higher precedence
            if (eof(index, tokens)) {
                return { index, result: lhs };
            }
            let rhs;
            let binOpToken = tokens[index];
            switch (binOpToken.kind) {
                // binary operators
                case "comma":
                    if (currentPrecedence > BinOpPrecedence.And) {
                        return { index, result: lhs };
                    }
                    const andRhsResult = parsePropertyFilterValueList(BinOpPrecedence.And, index + 1, tokens);
                    if (andRhsResult == null) {
                        // whitespace could follow, indicating the comma was for filter-and and not prop-filter-value-and
                        return { index, result: lhs };
                    }
                    ({ index, result: rhs } = andRhsResult);
                    lhs = { kind: "propand", a: lhs, b: rhs };
                    continue;
                case "pipe":
                    if (currentPrecedence > BinOpPrecedence.Or) {
                        return { index, result: lhs };
                    }
                    const orRhsResult = parsePropertyFilterValueList(BinOpPrecedence.Or, index + 1, tokens);
                    if (orRhsResult == null) {
                        return { index, result: lhs };
                    }
                    ({ index, result: rhs } = orRhsResult);
                    lhs = { kind: "propor", a: lhs, b: rhs };
                    continue;
                // end of value list
                case "whitespace":
                    return { index, result: lhs };
                case "closeparen":
                    // if we are somewhere within the parse tree, the closing paren could be handled by an upper recursion instance
                    if (currentPrecedence == BinOpPrecedence.Lowest) {
                        console.error("Unmatched close parenthesis in property value list at " + token.span[0]);
                    }
                    return { index, result: lhs };
                // invalid tokens
                case "openparen":
                case "int":
                case "comparison":
                case "word":
                case "dqstring":
                case "bang":
                case "colon":
                case "regex":
                    console.error("invalid token '" + binOpToken.kind + "' at " + binOpToken.span[0]);
                    return { index, result: lhs };
                default: assertNever(binOpToken);
            }
        }
    }
    function parsePropertyFilterValue(index, tokens) {
        if (eof(index, tokens)) {
            return null;
        }
        const not = tokens[index].kind == "bang";
        if (not) {
            index++;
            if (eof(index, tokens)) {
                return null;
            }
        }
        let filter;
        const numberFilterRes = parseNumberFilter(index, tokens);
        if (numberFilterRes != null) {
            ({ index, result: filter } = numberFilterRes);
        }
        else {
            const textRes = parseText(index, tokens);
            if (textRes != null) {
                let text;
                ({ index, result: text } = textRes);
                filter = { kind: "text", text };
            }
            else {
                const regexRes = parseRegex(index, tokens);
                if (regexRes == null) {
                    return null;
                }
                let regex;
                ({ index, result: regex } = regexRes);
                filter = { kind: "regex", regex };
            }
        }
        if (not) {
            filter = { kind: "propnot", filter };
        }
        return { index, result: filter };
    }
    /// Parses the number filter, returning the new index into the string and parsed NumFilter, or null if
    /// no NumFilter could be parsed.
    function parseNumberFilter(index, tokens) {
        if (eof(index, tokens)) {
            return null;
        }
        const token = tokens[index];
        switch (token.kind) {
            case "int":
                return { index: index + 1, result: { kind: "numfilter", typ: ComparisonType.Equals, number: token.number } };
            case "comparison":
                if (eof(index + 1, tokens)) {
                    return null;
                }
                const numberToken = tokens[index + 1];
                switch (numberToken.kind) {
                    case "int": return { index: index + 2, result: { kind: "numfilter", typ: token.typ, number: numberToken.number } };
                    default: return null;
                }
            default:
                return null;
        }
    }
    function parseText(index, tokens) {
        if (eof(index, tokens)) {
            return null;
        }
        const text = tokens[index];
        switch (text.kind) {
            case "dqstring":
            case "word":
                return { index: index + 1, result: text.text };
            default:
                return null;
        }
    }
    function parseWord(index, tokens) {
        if (eof(index, tokens)) {
            return null;
        }
        const token = tokens[index];
        switch (token.kind) {
            case "word": return { index: index + 1, result: token.text };
            default: return null;
        }
    }
    function parseRegex(index, tokens) {
        if (eof(index, tokens)) {
            return null;
        }
        const token = tokens[index];
        switch (token.kind) {
            case "regex": return { index: index + 1, result: token.regex };
            default: return null;
        }
    }
    /// Checks that the given token is at the given index of the token-array.
    function checkTokenKind(expectedKind, index, tokens) {
        if (eof(index, tokens)) {
            return null;
        }
        if (tokens[index].kind != expectedKind) {
            return null;
        }
        return { index: index + 1, result: undefined };
    }
    function consumeWhitespace(index, tokens) {
        let hasWhitespace = false;
        while (!eof(index, tokens) && tokens[index].kind == "whitespace") {
            hasWhitespace = true;
            index++;
        }
        return { index, result: hasWhitespace };
    }
    /** Returns if the index is larger than the array length. **/
    function eof(index, arr) {
        return index >= arr.length;
    }
    function applyParseFunction(index, tokens, func1, func2, func3, func4, func5, func6) {
        return applyParseFunctionsInternal(index, tokens, func1, func2, func3, func4, func5, func6);
    }
    function applyParseFunctionsInternal(index, tokens, ...funcs) {
        const returnValues = [];
        for (const func of funcs) {
            if (!func) {
                break;
            }
            const res = func(index, tokens);
            if (res == null) {
                return null;
            }
            let result;
            ({ index, result } = res);
            returnValues.push(result);
        }
        return { index, result: returnValues };
    }
    function assertNever(x) {
        throw new Error("Unexpected Object: " + x);
    }
})(Parser || (Parser = {}));

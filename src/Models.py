import json
import random as rand

import discord

import src.Util as mUtil
from src.KeyValueList import KeyValueList


# spell name is alway capitalize


class DonnyDiceEngine:
    def __init__(self, discrod_client, path_spell_book, path_casters, path_creatures):
        self._client: discord.Client = discrod_client
        self._spells: dict = self.init_data(path_spell_book)
        self._casters: dict = self.init_data(path_casters)
        self._creatures: dict = self.init_data(path_creatures)

    @staticmethod
    #   constructor support
    def init_data(json_path):
        return mUtil.mister_json_parserson(json_path)

    def discord_client(self):
        return self._client

    def list_spells(self):
        return self._spells.keys()

    def list_creatures(self):
        return self._creatures.keys()

    def list_casters(self):
        return self._casters.keys()

    def get_spells_by_type(self, type: str):
        ret = []
        for k in self._spells.keys():
            spell_types: KeyValueList = self._spells.get(k).get("type").split(", ")
            if type in spell_types:
                ret.append(k)
        print(ret)

    def get_spell(self, name):
        ret = self._spells.get(name, None)
        if ret is None:
            name = name.capitalize()
            if self.is_spell(name):
                return self._spells.get(name)
        return ret

    def get_creatures(self, name):
        if name not in self._creatures.keys():
            print("creature not found")
        return self._creatures.get(name)

    def get_character_name_by_player_id(self, player_id):
        player_id_str = str(player_id)
        try:
            return self._casters.get(player_id_str, None).get("character_name")
        except AttributeError:
            return None

    def cast_spell(self, caster_id: int, spell_name: str, target_name: str = "") -> str:
        caster_name = self.get_character_name_by_player_id(caster_id)

        if caster_name is None:
            ret = f"caster with id {caster_id} does not exists in player.json :/ a SERIOUS PROBLEM"
            return ret

        if target_name == "":
            ret = f"{caster_name} zaubert {spell_name}"
            ret += self.get_roll_feedback(caster_id)
        elif caster_name == target_name:
            ret = f"{caster_name} zaubert {spell_name} an sich selbst!"
            ret += self.get_roll_feedback(caster_id)
        else:
            ret = f"{caster_name} zaubert {spell_name} an {target_name.capitalize()}!"
            ret += self.get_roll_feedback(caster_id)
        return ret

    def get_roll_feedback(self, caster_id) -> str:
        ret = ""
        roll_direction = self.roll(1, 6) + self.get_modifier_direction(caster_id)
        ret += "\n" + self.feedback_direction(roll_direction)
        roll_strength = self.roll(1, 6) + self.get_modifier_strength(caster_id)
        ret += "\n" + self.feedback_strength(roll_strength)
        roll_effect = self.roll(1, 6) + self.get_modifier_effect(caster_id)
        ret += "\n" + self.feedback_effect(roll_effect)
        return ret

    def feedback_direction(self, roll_value: int) -> str:
        ret_str = ""
        if roll_value == 1:
            ret_str = f"Richtung: Komplett daneben!"
        elif roll_value == 2:
            ret_str = f"Richtung: Daneben!"
        elif roll_value in [3, 4]:
            ret_str = f"Richtung: Knapp dran!"
        elif roll_value == 5:
            ret_str = f"Richtung: Getroffen!"
        elif roll_value >= 6:
            print(f"roll_value was {roll_value}")
            ret_str = f"Richtung: Bull's Eye!"
        return ret_str

    def feedback_strength(self, roll_value: int) -> str:
        ret_str = ""
        if roll_value == 1:
            ret_str = f"Stärke: Schlapp..."
        elif roll_value == 2:
            ret_str = f"Stärke: Schwach!"
        elif roll_value in [3, 4]:
            ret_str = f"Stärke: So Mittel!"
        elif roll_value == 5:
            ret_str = f"Stärke: Stark!"
        elif roll_value >= 6:
            ret_str = f"Stärke: Umhauend!"
        return ret_str

    def feedback_effect(self, roll_value: int) -> str:
        ret_str = ""
        if roll_value == 1:
            ret_str = f"Effekt: Upsie!"
        elif roll_value == 2:
            ret_str = f"Effekt: Nichts passiert!"
        elif roll_value in [3, 4]:
            ret_str = f"Effekt: Ein wenig!"
        elif roll_value == 5:
            ret_str = f"Effekt: Genau richtig!"
        elif roll_value >= 6:
            ret_str = f"Effekt: Magisch!"
        return ret_str

    def is_spell(self, name: str) -> bool:
        spell_keys = self.list_spells()
        for key in spell_keys:
            if name.lower() == key.lower():
                return True
        return False

    def is_creature(self, name: str) -> bool:
        name = name.lower()
        for key in self.list_creatures():
            if name == key.lower():
                return True
        return False

    def is_player(self, name: str) -> bool:
        name = name.lower()
        list_caster_keys = self.list_casters()

        # look up start
        for id_key in list_caster_keys:
            player: dict = self._casters.get(id_key)
            nickname = player.get("nickname").lower()
            charname = player.get("character_name").lower()
            if name == nickname:
                return True
            if name == charname:
                return True
        return False

    def get_player_id_by_name(self, name) -> int:
        name = name.lower()
        list_caster_keys = self.list_casters()

        # look up start
        for id_key in list_caster_keys:
            player: dict = self._casters.get(id_key)
            nickname = player.get("nickname").lower()
            charname = player.get("character_name").lower()
            if name == nickname:
                return int(id_key)
            if name == charname:
                return int(id_key)
        return -1

    def get_player_by_id(self, player_id):
        list_player_id = self._casters.keys()
        if str(player_id) in list_player_id:
            return self._casters.get(str(player_id))

    def get_modifier_direction(self, player_id):
        player = self.get_player_by_id(str(player_id))
        return player.get("mod_richtung")

    def get_modifier_strength(self, player_id):
        player = self.get_player_by_id(str(player_id))
        return player.get("mod_staerke")

    def get_modifier_effect(self, player_id):
        player = self.get_player_by_id(str(player_id))
        return player.get("mod_effekt")

    def pretty_list_creature(self) -> str:
        ret = "----------------------------- Creatures ------------------------------\n"
        list_creature: list = list(self.list_creatures())
        ret += "```"
        while len(list_creature) != 0:
            ret += f"{list_creature.pop(0):20}"
            if len(list_creature) == 0:
                break
            ret += f"{list_creature.pop(0):20}"
            if len(list_creature) == 0:
                break
            ret += f"{list_creature.pop(0):20}\n"
        ret += "```"
        return ret

    def pretty_list_spells(self) -> str:
        ret = "------------------------------- Spells -------------------------------\n"
        list_spell: list = list(self.list_spells())
       
        c = 1
        while len(list_spell) != 0:
            ret += f"{list_spell.pop(0)}\n"
            c += 1
        return ret

    def pretty_spell_info(self, spell_name: str) -> str:
        spell: dict = self.get_spell(spell_name)
        spell_description = spell.get("description")
        ret = f"{spell_name.capitalize()}: \n" \
              f"{spell_description}"
        return ret

    def pretty_creature_info(self, creature_name: str) -> str:
        creature: dict = self.get_creatures(creature_name)
        creature_description = creature.get("description")
        ret = f"{creature_name.capitalize()}: \n" \
              f"{creature_description}"
        return ret

    def pretty_player_info(self, player_id) -> str:
        player = self.get_player_by_id(player_id)
        if player is None:
            return "Player not found"
        nickname = player.get("nickname")
        character_name = player.get("character_name")
        mod_direction = player.get("mod_richtung")
        mod_strength = player.get("mod_staerke")
        mod_effect = player.get("mod_effekt")
        ret = "```"  # ``` is for discord monospace font format
        ret += f"Nickname       : {nickname}\n"
        ret += f"Character name : {character_name}\n"
        ret += f"Richtung-Modifikator: {mod_direction}\n"
        ret += f"Stärke-Modifikator  : {mod_strength}\n"
        ret += f"Effekt-Modifikator  : {mod_effect}"
        ret += "```"  # the end of monospace format
        return ret

    def check(self, m: str) -> str:
        ret = ""
        split = m.split(" ")
        i0 = split[0]
        if split[0].capitalize() in self.list_spells():
            ret = f"{i0.capitalize()}!!!!"
        return ret

    def roll(self, n: int, d: int) -> int:
        return rand.randint(n, d)

    def roll_simple_str(self, text: str) -> int:
        split = ""
        if not is_dice_roll(text):
            return -1
        if text.find("w") > 0:
            split = text.split("w")
        elif text.find("d") > 0:
            split = text.split("d")
        n = int(split[0])
        d = int(split[1])
        s = 0
        for _ in range(n):
            s += rand.randint(1, d)
        return s

    def input_validation_service(self, user_input: str, user_id: int) -> str:
        ret = ""
        # expression at the end of text feedback.
        expression = ""
        input_split = user_input.split(" ")
        input_split_len = len(input_split)
        author_name = self.discord_client().get_user(user_id).name
        target_name = ""

        # check if "?" symbol is in user input
        sym_question: bool = "?" in user_input or "info" in user_input

        # clean up emotion:) by remove any additional "!" or "?"
        user_input = user_input.replace("!", "")
        user_input = user_input.replace("?", "")
        user_input = user_input.replace(" info", "")
        user_input = user_input.replace("info ", "")

        # split cleaned user input
        input_split = user_input.split(" ")
        input_split_len = len(input_split)

        # ?|info Player|Creature|Spell ?|info
        if sym_question:
            subject = user_input
            if self.is_spell(subject):
                ret = self.pretty_spell_info(subject)
            if self.is_creature(subject):
                ret = self.pretty_creature_info(subject)
            if self.is_player(subject):
                ret = self.pretty_player_info(self.get_player_id_by_name(subject))
            return ret

        # A simplest case of : !|_*SPELL!|_!* e.g. Accio! or Accio !!!! or Accio!!!!
        if input_split_len == 1:
            subject = user_input
            if self.is_spell(subject):
                ret = self.cast_spell(user_id, subject)
                return ret
            if is_dice_roll(subject):
                roll = str(self.roll_simple_str(subject))
                return f"{author_name} würfelt **{roll}**"

        else:
            # now, need to distinct the spell name then target type(Player or Creature) and name.
            spell_name = input_split[0]  # first word to begin comparing
            target: str = ""
            if not self.is_spell(spell_name):
                # get spell name by word matching.
                spell_keys = self.list_spells()
                for key in spell_keys:
                    key_split: str = key.split(" ")
                    if spell_name.lower() == key_split[0].lower():
                        # when first word matches, compare successive appended name and key.
                        # this method is faster then brut-force. (O(n* log^n))
                        for i in range(1, input_split_len):
                            spell_name += " " + input_split[i]
                            if spell_name.lower() == key.lower():
                                spell_name = key
                                # spell name is found!, spell_name is already updated, now just break free from loop.
                                break
            if self.is_spell(spell_name):

                # since we can have a target, we need to cut spell_name from user_input.
                #print(f"target is {user_input}")
                target = user_input.lower().replace(spell_name.lower(), "")
                #print(f"spell  is {spell_name}")
                #print(f"target is {target}")

                # if there is no target... just cast spell
                if target == "":
                    ret = self.cast_spell(user_id, spell_name)
                    return ret
                # split strings like (_*NAME_*)+  e.g. " Don The Cat" or "    Don    The    Cat     "
                target: list = target.split(" ")
                # remove all empty string.  ["", "Don", "The", "Cat"] to ["Don", "The", "Cat"]
                target.remove("")
                # join remaining strings with " " separator.
                target: str = " ".join(target)

                # since we have a target prepared, check if a target is a player OR a creature, else just print out.

                if self.is_player(target):
                    target_id = self.get_player_id_by_name(target)
                    target = self.get_character_name_by_player_id(target_id)
                    ret = self.cast_spell(user_id, spell_name, target)
                    return ret
                elif self.is_creature(target):
                    ret = self.cast_spell(user_id, spell_name, target)
                    return ret
                #target += f"\n(wer/was mag ein {target.capitalize()} sein?)"
                ret = self.cast_spell(user_id, spell_name, target)
            return ret

    def __str__(self):
        return self._spells.__str__()


def mister_json_parserson(json_path: str) -> KeyValueList:
    f = None
    # check input parameter, it must be a json file.
    split = str(json_path).split(".")
    file_type = split[split.__len__() - 1]
    if file_type != "json":
        raise Exception("File type must be json")
    try:
        f = open(json_path)
    except FileNotFoundError:
        print(f"A json file {json_path} does not exist")
    # load json
    with f as fo:
        k = KeyValueList(json.load(fo))
        return k


def is_dice_roll(m: str):
    dice = ""
    if m.find("w") > 0:
        dice = m.split("w")
    elif m.find("d") > 0:
        dice = m.split("d")
    if len(dice) == 2:
        if dice[0].isnumeric() and dice[1].isnumeric():
            return True
    return False


def roll(m: str) -> str:
    m = m.split("d")
    n = int(m[0])
    d = int(m[1])
    a = None
    b = None
    c = None
    ret = ""
    total: int = 0
    for i in range(n):
        if i == 0:
            a = rand.randint(1, d)
            ret += str(a) + ", "
        if i == 1:
            b = rand.randint(1, d)
            ret += str(b) + ", "
        if i == 2:
            c = rand.randint(1, d)
            ret += str(c) + " "
        total += rand.randint(1, d)
    return str(ret) + f" and total of {total}"

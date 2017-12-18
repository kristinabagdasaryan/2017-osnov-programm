import re
file = open('konstruktikon.xml')

#I create dictionaries to check whether they coincide with konstruktikon
roles = ["Actant", "Action", "Activity", "Addressee", "Agent", "Associated", "Beneficiary",
         "Cause", "Causee", "Causer", "Circumstance", "Condition", "Direction", "Distance",
         "Evaluation", "Event", "Experiencer", "Function", "Goal", "Goer", "Instrument", "Limit",
         "Location", "Manner", "Material", "Measure", "Motivation", "Participant", "Path", "Parameter",
         "Patient", "Phenomenon", "Property", "Purpose", "Protagonist", "Quantity", "Recipient", "Result",
         "Set", "Situation", "Source", "Speaker", "Standard", "State", "Theme", "Topic", "Undergoer"]

phrases = ['NP', 'VP', 'AP', 'AdvP', 'PP', 'NumP', 'XP', 'BareCl', 'IndirCl', 'Cl', 'S', 'DiscC',
           'DirSpeech', 'NP-Nom', 'NP-Gen', 'NP-Acc', 'NP-Dat', 'NP-Ins', 'NP-Loc', 'NP-Nom.Plur',
           'NP-Gen.Plur', 'NP-Acc.Plur', 'NP-Dat.Plur', 'NP-Ins.Plur', 'NP-Loc.Plur', 'NP-Nom.Sing',
           'NP-Gen.Sing', 'NP-Acc.Sing', 'NP-Dat.Sing', 'NP-Ins.Sing', 'NP-Loc.Sing', 'NP.Sing', 'NP.Plur',
           'VP-Inf', 'VP-Pres', 'VP-Past', 'VP-Fut', 'VP-Bare', 'VP-Imper', 'VP-Imp', 'VP-Perf', 'VP-Part',
           'VP-Pass', 'VP-Act', 'VP-Short', 'VP-Conv', 'VP-1Plur.Pres', 'VP-1Plur.Past', 'VP-1Plur.Fut',
           'VP-2Plur.Pres', 'VP-2Plur.Past', 'VP-2Plur.Fut', 'VP-3Plur.Pres', 'VP-3Plur.Past', 'VP-3Plur.Fut',
           'AP-Nom', 'AP-Gen', 'AP-Acc', 'AP-Dat', 'AP-Ins', 'AP-Loc', 'AP-Nom.Plur', 'AP-Gen.Plur', 'AP-Acc.Plur',
           'AP-Dat.Plur', 'AP-Ins.Plur', 'AP-Loc.Plur', 'AP-Nom.Sing', 'AP-Gen.Sing', 'AP-Acc.Sing', 'AP-Dat.Sing',
           'AP-Ins.Sing', 'AP-Loc.Sing', 'AP.Sing', 'AP.Plur', 'AP.Cmp', 'NUM', 'PART', 'PRON']

structures = ['nsubj', 'obj', 'iobj', 'csubj', 'ccomp', 'xcomp',
              'obl', 'advmod', 'cop', 'mark', 'nmod', 'nummod',
              'conj', 'cc', 'dep', 'root', 'amod', 'det', 'case', 'parataxis']

# at this step I do a parser to read an xml. file line by line and then extract the tags, that we need
def parser(text):
    n = 0
    blocks = []
    sense_block = False
    def_block = False
    find_konst_name = False
    find_struct = False
    block_dict = {}
    for line in text:
        n += 1
        #print(n)
        if not sense_block:
            if line.startswith('      <Sense id="konstruktikon-rus'):
                sense_block = True
                block_dict['sense'] = re.search('id="(.*?)--(.*?)"', line).group(2)
                block_dict['konst'] = []
                block_dict['def_names'] = []
                block_dict['structure'] = []
        else:
            if line.startswith('      </Sense>'):
                sense_block = False
                blocks.append(block_dict)
                block_dict = {}
            elif line.startswith('        <konst:int_const_elem'):
                konst_name = re.search('name="(.*?)"', line)
                if konst_name:
                    block_dict['konst'].append(re.search('name="(.*?)"', line).group(1))
                else:
                    find_konst_name = True
            elif find_konst_name:
                konst_name = re.search('name="(.*?)"', line)
                if konst_name:
                    block_dict['konst'].append(re.search('name="(.*?)"', line).group(1))
                else:
                    find_konst_name = False
            elif line.startswith('        <feat att="structure"'):
                struct_val = re.search('val="(.*?)"', line)
                if struct_val:
                    block_dict['structure'].append(re.search('val="(.*?)"', line).group(1))
                else:
                    find_struct = True
            elif find_struct:
                struct_val = re.search('val="(.*?)"', line)
                if struct_val:
                    block_dict['structure'].append(re.search('val="(.*?)"', line).group(1))
                else:
                    find_struct = False

            if not def_block:
                if line.startswith('        <definition>'):
                    def_block = True
            else:
                if line.startswith('          <karp:e'):
                    block_dict['def_names'].append(re.search('name="(.*?)"', line).group(1))
                elif line.startswith('        </definition>'):
                    def_block = False
    return blocks

#1. I look at the name of construction and
# check that each token in the name is the same
# as the "name" in the Construction elements, internal
#if not, than we create a file with fail constructions

def check_konst_names(sense_str, konst_list):
    fail = False
    for token in sense_str.split('_'):
        token = token.strip('?!):,')
        token = re.sub('\(', '', token)
        if token not in konst_list:
            fail = True
    return fail

#2. I look at the definitions and check that each role coincides
# with the existing roles in the dictionary
# if there is a role, that do not exist in the dictionary, than it is stored
# in a new file with fail constructions
def check_definitions(def_names, roles=roles):
    fail = False
    for token in def_names:
        token = token.strip('.,?!:')
        if token not in roles:
            fail = True
    return fail

#3. I look at the name of the constructions and check that each phrase or POS coincides
# with the existing phrases in the dictionary
# if there is a phrase or POS, that do not exist in the dictionary, than it is stored
# in a new file with fail constructions
def check_tokens(sense_str, phrases=phrases):
    fail = False
    eng = 'qwertyuiopasdfghjklzxcvbnm'
    for token in sense_str.split('_'):
        token = token.strip('?!):,')
        token = re.sub('\(', '', token)
        if len(token) > 0 and token[0].lower() in eng:
            if token not in phrases:
                fail = True
    return fail

#4. I look at the structure and check that each relation coincides
# with the existing relations in the dictionary
# if there is a relation, that do not exist in the dictionary, than it is stored
# in a new file with fail constructions
def check_sctructs(struct_list, structures_proper_list=structures):
    fail = False
    eng = 'qwertyuiopasdfghjklzxcvbnm'
    for structure in struct_list:
        for token in structure.split():
            if token.startswith('['):

                if len(token) > 1 and token[1].lower() in eng:
                    if token[1:] not in structures_proper_list:
                        fail = True
    return fail


file1 = open('konst_check.txt', 'w')
file2 = open('def_check.txt', 'w')
file3 = open('sense_id_check.txt', 'w')
file4 = open('structure_check.txt', 'w')
for block in parser(file):
    if check_konst_names(block['sense'], block['konst']):
        file1.write(block['sense'] + '\n')
    if check_definitions(block['def_names']):
        file2.write(block['sense'] + '\n')
    if check_tokens(block['sense']):
        file3.write(block['sense'] + '\n')
    if check_sctructs(block['structure']):
        file4.write(block['sense'] + '\n')
file1.close()
file2.close()
file3.close()
file4.close()

file.close()

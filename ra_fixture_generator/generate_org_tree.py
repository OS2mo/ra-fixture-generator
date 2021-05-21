import random

from mimesis import Address


def generate_cantina():
    if random.random() > 0.5:
        return {"Kantine": {}}
    return {}


def gen_schools_and_childcare(seed, num_schools=30, num_childcare=20):
    address_gen = Address('da', seed=seed)

    def generate_school(_):
        name = address_gen.city() + " skole"
        return name, {}

    def generate_childcare(_):
        name = address_gen.city() + " børnehus"
        if random.random() > 0.5:
            return name, {"Administration": {}}
        if random.random() > 0.5:
            return name, {"Teknisk Support": {}}
        return name, {}

    ret = {}
    ret.update(dict(map(generate_school, range(num_schools))))
    ret.update(dict(map(generate_childcare, range(num_childcare))))
    return ret


def gen_org_tree(seed):
    random.seed(seed)
    org_tree = {
        'Borgmesterens Afdeling': {
            'Budget og Planlægning': {},
            'HR og organisation': {},
            'Erhverv': {},
            'Byudvikling': {},
            'IT-Support': {},
        },
        'Teknik og Miljø': {
            'Kloakering': generate_cantina(),
            'Park og vej': generate_cantina(),
            'Renovation': generate_cantina(),
            'Belysning': generate_cantina(),
            'IT-Support': generate_cantina(),
        },
        'Skole og Børn': {
            'Social Indsats': {
                "Skole og børnehaver": gen_schools_and_childcare(seed),
            },
            'IT-Support': generate_cantina(),
        },
        'Social og sundhed': {},
    }
    return org_tree


def tree_visitor(tree, yield_func, level=1, prefix=""):
    for name, children in tree.items():
        yield yield_func(name, level, prefix)
        yield from tree_visitor(children, yield_func, level+1, prefix + name)


def tree_visitor_levels(tree, yield_func, level=1, prefix=""):
    for name, children in tree.items():
        yield yield_func(name, level, prefix)
    for name, children in tree.items():
        yield from tree_visitor_levels(children, yield_func, level+1, prefix + name)


if __name__ == "__main__":
    random_seed = "0xFF"
    org_tree = gen_org_tree(random_seed)
    print(org_tree)

    def yield_func(name, level, prefix):
        return "  " * (level - 1) + name

    for string in list(tree_visitor(org_tree, yield_func)):
        print(string)

    for string in list(tree_visitor_levels(org_tree, yield_func)):
        print(string)

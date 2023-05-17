def filter_artifacts(activities_artifacts):
    return list(filter(lambda x: x['Type (Activity/Artifact)'] == 'artifact', activities_artifacts))


def filter_activities(activities_artifacts):
    return list(filter(lambda x: x['Type (Activity/Artifact)'] == 'activity', activities_artifacts))


def map_art_cats_to_act_cats(categories):
    mapping = []
    for category, cats in categories.items():
        art_cats = []
        for cat in cats:
            if cat['Artifact Category'] not in art_cats and cat['Input/Intermediate/Output'] != 'Intermediate':
                art_cats.append(cat['Artifact Category'])
                mapping.append((category, cat['Artifact Category'], cat['Artifact Category Description'], cat['Input/Intermediate/Output']))
    return mapping

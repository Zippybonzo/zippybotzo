import pywikibot
import mwparserfromhell

def print_template_params(wikicode, section, target_template_name):
    page = pywikibot.Page(pywikibot.Site(), "User:ZippyBotZo/Test")
    for template in section.filter_templates():
        if template.name.strip() == target_template_name:
            params = {param.name.strip(): param.value.strip() for param in template.params}
            page1name = params.get('1')
            page2name = params.get('2')
            page1 = pywikibot.Page(pywikibot.Site(), page1name)
            page2 = pywikibot.Page(pywikibot.Site(), page2name)
            protection1 = page1.protection()
            protection2 = page2.protection()
            if protection1.get('move', (None,))[0] == 'sysop' or protection1.get('edit', (None,))[0] == 'sysop':
                # Move the template to the administrator needed section
                template = "\n* " + str(template)
                admin_section = wikicode.get_sections(matches="Administrator needed")
                if admin_section:
                    admin_section[0].append(template)
                    wikicode.append(admin_section[0])
                else:
                    new_section = mwparserfromhell.nodes.Section(
                        "== Administrator needed ==",
                        [template]
                    )
                    wikicode.append(new_section)
                page.text = str(wikicode)
            if page2.exists():
                if protection2.get('move', (None,))[0] == 'sysop' or protection2.get('edit',    (None,))[0] == 'sysop':
                    print(f"{page2name} is protected by sysop")
    page.save()
def run():
    site = pywikibot.Site("test", "wikipedia")
    page = pywikibot.Page(site, "User:ZippyBotZo/Test")
    wikicode = mwparserfromhell.parse(page.text)
    
    target_template_name = "RMassist/core"
    
    for section in wikicode.get_sections(levels=[2,3,4,5,6]):
        print_template_params(wikicode, section, target_template_name)

main()
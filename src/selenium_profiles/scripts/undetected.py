def exec_cdp(driver, cdp_tools=None):
    if cdp_tools is None:
        from selenium_profiles.scripts.cdp_tools import cdp_tools
        cdp_tools = cdp_tools(driver)

    # set webdriver js var to false
    cdp_tools.evaluate_on_new_document("""
                                            Object.defineProperty(window, 'navigator', {
                                                value: new Proxy(navigator, {
                                                        has: (target, key) => (key === 'webdriver' ? false : key in target),
                                                        get: (target, key) =>
                                                                key === 'webdriver' ?
                                                                false :
                                                                typeof target[key] === 'function' ?
                                                                target[key].bind(target) :
                                                                target[key]
                                                        })
                                            });
                                            """)

    def get_cdc_props():  # if true ==> detectable
        return driver.execute_script(
            """
            let objectToInspect = window,
                result = [];
            while(objectToInspect !== null)
            { result = result.concat(Object.getOwnPropertyNames(objectToInspect));
              objectToInspect = Object.getPrototypeOf(objectToInspect); }
            return result.filter(i => i.match(/.+_.+_(Array|Promise|Symbol)/ig))
            """
        )

    if get_cdc_props():
        cdp_tools.evaluate_on_new_document("""
                                                    let objectToInspect = window,
                                                        result = [];
                                                    while(objectToInspect !== null) 
                                                    { result = result.concat(Object.getOwnPropertyNames(objectToInspect));
                                                      objectToInspect = Object.getPrototypeOf(objectToInspect); }
                                                    result.forEach(p => p.match(/.+_.+_(Array|Promise|Symbol)/ig)
                                                                        &&delete window[p]&&console.log('removed',p))
                                                    """)

        if cdp_tools is None:
            return cdp_tools.evaluate_on_document_identifiers


def config_options(options):
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.arguments.extend(["--disable-blink-features=AutomationControlled", "--disable-blink-features"])

    # suppress welcome
    options.arguments.extend(["--no-default-browser-check", "--no-first-run"])

    return options

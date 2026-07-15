from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError


async def crawl_website(url: str, timeout: int = 30) -> dict:
    browser = None
    try:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=timeout * 1000
        )

        extracted_data = await page.evaluate("""
            () => {
                const getAttrs = (el) => {
                    const attrs = {};
                    for (let i = 0; i < el.attributes.length; i++) {
                        const attr = el.attributes[i];
                        if (!['style', 'class'].includes(attr.name)) {
                            attrs[attr.name] = attr.value;
                        }
                    }
                    return attrs;
                };
                return {
                    html: document.documentElement.outerHTML,
                    images: Array.from(document.querySelectorAll('img')).map(e => ({
                        tag: 'img',
                        attributes: getAttrs(e)
                    })),
                    buttons: Array.from(document.querySelectorAll(
                        'button, input[type="button"], input[type="submit"], [role="button"]'
                    )).map(e => ({
                        tag: e.tagName.toLowerCase(),
                        text: e.innerText?.trim() || '',
                        attributes: getAttrs(e)
                    })),
                    forms: Array.from(document.querySelectorAll('form')).map(e => ({
                        tag: 'form',
                        attributes: getAttrs(e)
                    })),
                    links: Array.from(document.querySelectorAll('a[href]')).map(e => ({
                        tag: 'a',
                        text: e.innerText?.trim() || '',
                        attributes: getAttrs(e)
                    })),
                    headings: Array.from(document.querySelectorAll(
                        'h1, h2, h3, h4, h5, h6'
                    )).map(e => ({
                        tag: e.tagName.toLowerCase(),
                        text: e.innerText?.trim() || '',
                        attributes: getAttrs(e)
                    }))
                };
            }
        """)
        return extracted_data

    except PlaywrightTimeoutError:
        raise Exception(
            f"Timeout: Website took too long to load ({timeout}s limit). "
            "Try a simpler page or increase the timeout."
        )
    except Exception as e:
        error_msg = str(e)
        if "net::ERR_NAME_NOT_RESOLVED" in error_msg:
            raise Exception("Invalid website: Domain could not be found.")
        if "net::ERR_CONNECTION_REFUSED" in error_msg:
            raise Exception("Connection refused by the server.")
        if "net::ERR_CONNECTION_TIMED_OUT" in error_msg:
            raise Exception("Connection timed out. The server is not responding.")
        raise Exception(f"Failed to crawl website: {error_msg}")
    finally:
        if browser:
            try:
                await browser.close()
            except Exception:
                pass
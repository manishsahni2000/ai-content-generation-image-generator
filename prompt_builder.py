def build_prompt(brief, product):
    template = brief.get("prompt_template") or \
        "A campaign image of {product} for {target_audience} in {target_region}, showing '{campaign_message}'."
    return template.format(
        product=product,
        target_audience=brief.get("target_audience", "general audience"),
        target_region=brief.get("target_region", "unknown region"),
        campaign_message=brief.get("campaign_message", "")
    )
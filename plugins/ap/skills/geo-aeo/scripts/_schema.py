"""_schema.py — JSON-LD lint: required/recommended properties per type, graph wiring, and
facts that contradict the page.

Required = Google's documented minimum for the rich result (or schema.org sense where Google
has no feature). Recommended = what makes the entity unambiguous to a knowledge graph or an
LLM reading the block. Keep in sync with references/structured-data.md.
"""
from __future__ import annotations

import re

from _page import types_of

# type -> (required, recommended). Dotted paths are checked one level deep.
RULES: dict[str, tuple[list, list]] = {
    "Organization": ([  "name"], ["url", "logo", "sameAs", "description", "contactPoint", "legalName", "address", "@id"]),
    "LocalBusiness": (["name", "address"], ["telephone", "url", "geo", "openingHoursSpecification", "image", "priceRange", "sameAs", "@id", "areaServed"]),
    "WebSite": (["name", "url"], ["@id", "publisher", "alternateName", "inLanguage"]),
    "WebPage": ([], ["name", "url", "isPartOf", "about", "dateModified", "primaryImageOfPage", "breadcrumb"]),
    "Article": (["headline"], ["author", "datePublished", "dateModified", "image", "publisher", "mainEntityOfPage"]),
    "BlogPosting": (["headline"], ["author", "datePublished", "dateModified", "image", "publisher", "mainEntityOfPage"]),
    "NewsArticle": (["headline"], ["author", "datePublished", "dateModified", "image", "publisher"]),
    "TechArticle": (["headline"], ["author", "datePublished", "dateModified", "image"]),
    "Person": (["name"], ["url", "sameAs", "jobTitle", "worksFor", "image", "description", "knowsAbout"]),
    "BreadcrumbList": (["itemListElement"], []),
    "Product": (["name"], ["image", "description", "sku", "brand", "offers", "aggregateRating", "review", "gtin", "mpn"]),
    "ProductGroup": (["name"], ["hasVariant", "variesBy", "productGroupID", "brand"]),
    "Offer": (["price", "priceCurrency"], ["availability", "url", "priceValidUntil", "hasMerchantReturnPolicy", "shippingDetails", "itemCondition"]),
    "AggregateOffer": (["lowPrice", "priceCurrency"], ["highPrice", "offerCount"]),
    "AggregateRating": (["ratingValue"], ["ratingCount", "reviewCount", "bestRating"]),
    "Review": (["author", "reviewRating"], ["itemReviewed", "datePublished", "reviewBody"]),
    "MerchantReturnPolicy": (["applicableCountry", "returnPolicyCategory"], ["merchantReturnDays", "returnMethod", "returnFees"]),
    "OfferShippingDetails": (["shippingDestination", "shippingRate", "deliveryTime"], []),
    "FAQPage": (["mainEntity"], []),
    "QAPage": (["mainEntity"], []),
    "Question": (["name"], ["acceptedAnswer", "suggestedAnswer", "answerCount"]),
    "HowTo": (["name", "step"], ["totalTime", "supply", "tool", "image"]),
    "Event": (["name", "startDate", "location"], ["endDate", "eventStatus", "eventAttendanceMode", "offers", "organizer", "image", "description"]),
    "Recipe": (["name", "image"], ["author", "recipeIngredient", "recipeInstructions", "totalTime", "nutrition", "aggregateRating"]),
    "VideoObject": (["name", "thumbnailUrl", "uploadDate"], ["description", "duration", "contentUrl", "embedUrl", "hasPart"]),
    "SoftwareApplication": (["name", "offers"], ["applicationCategory", "operatingSystem", "aggregateRating", "review"]),
    "WebApplication": (["name", "offers"], ["applicationCategory", "operatingSystem", "aggregateRating", "review"]),
    "MobileApplication": (["name", "offers"], ["applicationCategory", "operatingSystem", "aggregateRating", "review"]),
    "Service": (["name"], ["provider", "areaServed", "serviceType", "description", "offers"]),
    "Course": (["name", "description"], ["provider", "offers", "hasCourseInstance"]),
    "JobPosting": (["title", "description", "datePosted", "hiringOrganization", "jobLocation"], ["validThrough", "employmentType", "baseSalary"]),
    "Dataset": (["name", "description"], ["license", "creator", "distribution", "temporalCoverage"]),
    "ProfilePage": (["mainEntity"], ["dateCreated", "dateModified"]),
    "DiscussionForumPosting": (["author", "datePublished"], ["text", "headline", "url", "interactionStatistic"]),
    "ImageObject": ([], ["license", "acquireLicensePage", "creator", "creditText", "copyrightNotice"]),
}
LOCAL_SUBTYPES = re.compile(
    r"((?<!Online)Store|Restaurant|Clinic|Dentist|Physician|Hospital|Pharmacy|AutoRepair|AutoDealer|Bakery|CafeOrCoffeeShop|"
    r"BarOrPub|Hotel|LodgingBusiness|BeautySalon|HairSalon|DaySpa|HealthClub|Gym|LegalService|Attorney|Notary|"
    r"AccountingService|FinancialService|RealEstateAgent|HomeAndConstructionBusiness|Electrician|Plumber|"
    r"HVACBusiness|Locksmith|MovingCompany|RoofingContractor|GeneralContractor|ProfessionalService|"
    r"EmploymentAgency|TravelAgency|ChildCare|School|AnimalShelter|VeterinaryCare|FoodEstablishment|"
    r"EntertainmentBusiness|SportsActivityLocation|AutomotiveBusiness|MedicalBusiness|Optician)$"
)
# Types Google no longer shows as rich results for most sites; still valid schema.org.
LIMITED = {
    "FAQPage": "Google stopped showing FAQ rich results entirely on 2026-05-07 (gov/health-only since 2023). Valid, harmless, no rich-result lever; keep it only if the Q&A is visible on the page.",
    "HowTo": "HowTo rich results were removed from Google in Sept 2023. Valid, harmless, not a rich-result lever.",
    "Course": "Google retired the Course Info rich result in June 2025 (Course list carousel may still apply).",
    "ClaimReview": "Google retired ClaimReview rich results in June 2025.",
    "SpecialAnnouncement": "Retired by Google in June 2025.",
    "Dataset": "Dataset markup now serves Google Dataset Search only, not web results.",
}


def _has(obj: dict, key: str) -> bool:
    v = obj.get(key)
    return v not in (None, "", [], {})


def _visible_number(v, text: str) -> bool:
    try:
        f = float(str(v).replace(",", ""))
    except ValueError:
        return str(v) in text
    forms = {str(v), f"{f:.2f}", f"{f:,.2f}", f"{f:g}", f"{f:,.0f}" if f == int(f) else f"{f:g}", f"{int(f)}" if f == int(f) else f"{f}"}
    t = text.replace("\u00a0", " ")
    return any(re.search(r"(?<![\d.])" + re.escape(x) + r"(?![\d])", t) for x in forms if x)


def lint(objects: list[dict], page_url: str = "", page_text: str = "") -> list[dict]:
    """Return findings: {severity, type, message}."""
    out: list[dict] = []
    ids: dict[str, int] = {}
    all_types: list[str] = []

    def walk(o, depth=0):
        if not isinstance(o, dict) or depth > 6:
            return
        ts = types_of(o)
        all_types.extend(ts)
        if o.get("@id"):
            ids[o["@id"]] = ids.get(o["@id"], 0) + 1
        for t in ts:
            rule = RULES.get(t)
            if rule is None and LOCAL_SUBTYPES.search(t):
                rule = RULES["LocalBusiness"]
            if rule is None:
                continue
            req, rec = rule
            service_area = not _has(o, "address") and (_has(o, "areaServed") or t in ("ProfessionalService", "LocalBusiness") and _has(o, "serviceArea"))
            for k in req:
                if not _has(o, k):
                    if k == "address" and (service_area or t == "ProfessionalService"):
                        if depth == 0:
                            out.append({"severity": "info", "type": t, "message": f"{t} without an address: fine for a service-area / online business when areaServed is set. Never add a fake or virtual-office address; if there is no public premises, Organization + areaServed is the cleaner type"})
                    else:
                        out.append({"severity": "high", "type": t, "message": f"{t} is missing required '{k}'"})
            skip = {"geo", "openingHoursSpecification", "address", "priceRange"} if not _has(o, "address") else set()
            miss = [k for k in rec if not _has(o, k) and k not in skip]
            if miss and depth == 0:
                out.append({"severity": "low", "type": t, "message": f"{t} could add: {', '.join(miss)}"})
            if t in LIMITED and depth == 0:
                out.append({"severity": "info", "type": t, "message": LIMITED[t]})
            _specific(t, o, out, page_text)
        for k, v in o.items():
            if k.startswith("@"):
                continue
            if isinstance(v, dict):
                walk(v, depth + 1)
            elif isinstance(v, list):
                for x in v:
                    walk(x, depth + 1)

    for o in objects:
        if not isinstance(o, dict):
            continue
        ctx = str(o.get("@context", ""))
        if ctx and "schema.org" not in ctx:
            out.append({"severity": "medium", "type": "?", "message": f"@context is '{ctx[:60]}', not schema.org"})
        if not o.get("@type"):
            out.append({"severity": "medium", "type": "?", "message": "JSON-LD object without @type"})
        walk(o)

    if len(objects) > 1 and not any(isinstance(o, dict) and o.get("@id") for o in objects):
        out.append({"severity": "low", "type": "graph", "message": "Several JSON-LD entities with no @id: link them into one @graph (WebPage isPartOf WebSite, publisher -> Organization @id) so parsers see one connected entity."})
    return out


def _specific(t: str, o: dict, out: list, page_text: str):
    if t in ("Article", "BlogPosting", "NewsArticle", "TechArticle"):
        a = o.get("author")
        if isinstance(a, str):
            out.append({"severity": "medium", "type": t, "message": "author is a bare string; use a Person (or Organization) object with name + url (+ sameAs)"})
        elif isinstance(a, dict) and not (a.get("url") or a.get("sameAs") or a.get("@id")):
            out.append({"severity": "low", "type": t, "message": "author Person has no url/sameAs: link it to an author page so the byline resolves to an entity"})
        for k in ("datePublished", "dateModified"):
            v = o.get(k)
            if v and not re.match(r"^\d{4}-\d{2}-\d{2}", str(v)):
                out.append({"severity": "medium", "type": t, "message": f"{k} '{v}' is not ISO 8601"})
            elif v and "T" in str(v) and not re.search(r"(Z|[+-]\d{2}:?\d{2})$", str(v)):
                out.append({"severity": "low", "type": t, "message": f"{k} '{v}' has a time but no timezone"})
    if t == "Organization" or LOCAL_SUBTYPES.search(t) or t == "LocalBusiness":
        s = o.get("sameAs")
        if s is None:
            pass
        elif isinstance(s, str):
            s = [s]
        if isinstance(s, list) and len(s) < 2:
            out.append({"severity": "low", "type": t, "message": "sameAs lists fewer than 2 profiles; add every official profile (LinkedIn, Wikidata, Crunchbase, GBP/Maps, socials)"})
    if t == "ImageObject" and not (o.get("contentUrl") or o.get("url")):
        out.append({"severity": "medium", "type": t, "message": "ImageObject has neither contentUrl nor url"})
    if t in ("Offer",):
        p = o.get("price")
        if isinstance(p, str) and re.search(r"[^\d.]", p):
            out.append({"severity": "high", "type": t, "message": f"price '{p}' must be a number without currency symbols or separators"})
        elif p not in (None, "") and page_text and not _visible_number(p, page_text):
            out.append({"severity": "high", "type": t, "message": f"price {p} is in JSON-LD but not visible on the page — live-fetching AI tools read only visible text, and hidden-only markup breaks Google policy"})
    if t == "AggregateRating" and page_text:
        rv = o.get("ratingValue")
        if rv not in (None, "") and not _visible_number(rv, page_text):
            out.append({"severity": "medium", "type": t, "message": f"ratingValue {rv} is not visible on the page; show the rating and review count as text"})
    if t in ("Article", "BlogPosting", "NewsArticle", "TechArticle"):
        a = o.get("author")
        names = [a.get("name", "")] if isinstance(a, dict) else [x.get("name", "") for x in a if isinstance(x, dict)] if isinstance(a, list) else []
        for n in names:
            if n and re.match(r"(?i)^(by|posted by)\b|,| and ", n):
                out.append({"severity": "medium", "type": t, "message": f"author.name '{n}' should be one person's name only (no 'By', titles, or several names)"})
            elif n and page_text and n.lower() not in page_text.lower():
                out.append({"severity": "medium", "type": t, "message": f"author '{n}' is in schema but no visible byline shows it"})
    if t == "AggregateRating":
        if not (o.get("ratingCount") or o.get("reviewCount")):
            out.append({"severity": "high", "type": t, "message": "AggregateRating needs ratingCount or reviewCount"})
    if t == "FAQPage" and page_text:
        me = o.get("mainEntity") or []
        if isinstance(me, dict):
            me = [me]
        unseen = 0
        for q in me:
            name = (q or {}).get("name", "") if isinstance(q, dict) else ""
            if name and name[:40].lower() not in page_text.lower():
                unseen += 1
        if unseen:
            out.append({"severity": "high", "type": t, "message": f"{unseen} FAQ question(s) in markup are not visible on the page — markup must match visible content (spam policy)"})

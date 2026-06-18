from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from apps.visas.models import Country, VisaType, DocumentRequirement


DATA = [

    # =========================================================================
    # GROUP 1: CORE BIG FIVE
    # =========================================================================
    {
        "country": {"name": "United Kingdom", "code": "GBR", "flag_emoji": "🇬🇧"},
        "visa_type": {
            "name": "UK Business Visitor Visa",
            "category": "business",
            "processing_time": "3–6 weeks",
            "fee_usd": "115.00",
            "tips": "Required for attending conferences, meetings, or training. Ensure you have an invitation letter from the UK company.",
            "validity": "6 months",
            "description": "The Business Visitor Visa allows Nigerian nationals to visit the UK for short-term business activities like conferences or meetings."
        },
        "documents": [
            {
                "name": "Valid International Passport",
                "description": "Current passport with at least one blank page and 6 months validity.",
                "icon_category": "passport",
                "importance": "mandatory",
                "sample_description": "Must not be damaged. Include old passports to show travel history.",
                "common_mistakes": "Providing a passport expiring soon.",
                "official_source_url": "https://www.gov.uk/standard-visitor/apply-standard-visitor-visa"
            },
            {
                "name": "Invitation Letter",
                "description": "Letter from the UK host company detailing the purpose and duration of the trip.",
                "icon_category": "employment",
                "importance": "mandatory",
                "sample_description": "Must be on company letterhead, signed, and specify if they are covering your expenses.",
                "common_mistakes": "Missing contact details of the UK host or vague event description."
            }
        ]
    },
    {
        "country": {"name": "United Kingdom", "code": "GBR", "flag_emoji": "🇬🇧"},
        "visa_type": {
            "name": "UK Standard Visitor Visa",
            "category": "tourist",
            "processing_time": "3–6 weeks",
            "fee_usd": "115.00",
            "tips": "Fee is typically paid online in USD. Expect to pay around ₦172,500 based on black market rates. Avoid using new bank accounts.",
            "validity": "6 months",
            "description": (
                "The Standard Visitor Visa allows Nigerian nationals to visit the UK for tourism, "
                "business meetings, or family visits for up to 6 months. Applications are submitted "
                "online via GOV.UK and biometrics are enrolled at a VFS Global centre in Nigeria. "
                "Refusal rates for Nigerians are high — strong financial ties to Nigeria and a clear "
                "travel itinerary significantly improve approval chances."
            ),
        },
        "documents": [
            {
                "order": 1, "name": "International Passport", "icon_category": "passport",
                "importance": "mandatory", "condition_note": "",
                "description": "Valid travel document for UK entry.",
                "sample_description": "Must be valid for the full duration of stay. Include all previous passports showing travel history.",
                "official_source_url": "https://www.gov.uk/standard-visitor/apply-standard-visitor-visa",
                "last_verified": "2026-06-01",
            },
            {
                "order": 2, "name": "Completed Online Application (VAF1A)", "icon_category": "other",
                "importance": "mandatory", "condition_note": "",
                "description": "The official UK visa application form.",
                "sample_description": "Complete at gov.uk/apply-uk-visa. Print the confirmation page with your IHS reference number.",
                "official_source_url": "https://www.gov.uk/standard-visitor/apply-standard-visitor-visa",
                "last_verified": "2026-06-01",
            },
            {
                "order": 3, "name": "Passport Photographs", "icon_category": "photo",
                "importance": "mandatory", "condition_note": "",
                "description": "Recent biometric photos.",
                "sample_description": "2 recent colour photos, 45mm x 35mm, white background, taken within the last 6 months.",
                "official_source_url": "https://www.gov.uk/standard-visitor/apply-standard-visitor-visa",
                "last_verified": "2026-06-01",
            },
            {
                "order": 4, "name": "Bank Statements", "icon_category": "financial",
                "importance": "mandatory", "condition_note": "",
                "description": "Proof of sufficient funds to cover the trip.",
                "sample_description": "6 months of personal bank statements showing consistent balance. Minimum recommended: £2,000+. Must show your name, account number, and all transactions.",
                "official_source_url": "https://www.gov.uk/standard-visitor/apply-standard-visitor-visa",
                "last_verified": "2026-06-01",
            },
            {
                "order": 5, "name": "Proof of Employment / Business Ownership", "icon_category": "employment",
                "importance": "mandatory", "condition_note": "",
                "description": "Evidence of economic ties to Nigeria.",
                "sample_description": "Employer letter on company letterhead stating your role, salary, and approved leave dates. Self-employed: CAC certificate and 6 months of business account statements.",
                "official_source_url": "https://www.gov.uk/standard-visitor/apply-standard-visitor-visa",
                "last_verified": "2026-06-01",
            },
            {
                "order": 6, "name": "Payslips", "icon_category": "financial",
                "importance": "mandatory", "condition_note": "",
                "description": "Proof of regular income.",
                "sample_description": "Last 3–6 months of payslips corresponding to your bank deposits.",
                "official_source_url": "https://www.gov.uk/standard-visitor/apply-standard-visitor-visa",
                "last_verified": "2026-06-01",
            },
            {
                "order": 7, "name": "Travel Itinerary", "icon_category": "travel",
                "importance": "mandatory", "condition_note": "",
                "description": "Planned travel schedule.",
                "sample_description": "Flight booking confirmation (not necessarily paid ticket) and hotel booking for your intended dates.",
                "official_source_url": "https://www.gov.uk/standard-visitor/apply-standard-visitor-visa",
                "last_verified": "2026-06-01",
            },
            {
                "order": 8, "name": "Accommodation Proof", "icon_category": "accommodation",
                "importance": "mandatory", "condition_note": "",
                "description": "Where you will stay in the UK.",
                "sample_description": "Hotel booking confirmation or an invitation letter from a UK host with their proof of address and immigration status.",
                "official_source_url": "https://www.gov.uk/standard-visitor/apply-standard-visitor-visa",
                "last_verified": "2026-06-01",
            },
            {
                "order": 9, "name": "Travel History", "icon_category": "travel",
                "importance": "optional", "condition_note": "",
                "description": "Previous international travel.",
                "sample_description": "Copies of visa pages and entry/exit stamps from prior travel, especially to the US, Canada, Schengen, or other UK visas.",
                "official_source_url": "https://www.gov.uk/standard-visitor/apply-standard-visitor-visa",
                "last_verified": "2026-06-01",
            },
            {
                "order": 10, "name": "Proof of Property Ownership", "icon_category": "financial",
                "importance": "conditional", "condition_note": "Only if you own property in Nigeria.",
                "description": "Demonstrates strong ties to Nigeria.",
                "sample_description": "Land title documents, property deed, or tenancy agreement in your name.",
                "official_source_url": "https://www.gov.uk/standard-visitor/apply-standard-visitor-visa",
                "last_verified": "2026-06-01",
            },
            {
                "order": 11, "name": "Letter of Invitation", "icon_category": "other",
                "importance": "conditional", "condition_note": "Only if staying with a UK host.",
                "description": "From a UK-based host.",
                "sample_description": "Host's letter explaining relationship, planned activities, and willingness to accommodate. Must attach their proof of address and leave to remain / British passport copy.",
                "official_source_url": "https://www.gov.uk/standard-visitor/apply-standard-visitor-visa",
                "last_verified": "2026-06-01",
            },
            {
                "order": 12, "name": "Yellow Fever Vaccination Card", "icon_category": "medical",
                "importance": "mandatory", "condition_note": "",
                "description": "Required for travellers from Nigeria.",
                "sample_description": "Original yellow card issued by a certified Nigerian health authority.",
                "official_source_url": "https://www.gov.uk/standard-visitor/apply-standard-visitor-visa",
                "last_verified": "2026-06-01",
            },
        ],
    },

    {
        "country": {"name": "United States", "code": "USA", "flag_emoji": "🇺🇸"},
        "visa_type": {
            "name": "US B-1/B-2 Visitor Visa",
            "category": "tourist",
            "processing_time": "3–6 months (interview wait times are long in Lagos)",
            "fee_usd": "185.00",
            "tips": "The MRV fee must be paid at GTBank or via their online platform. It costs exactly ₦231,250 depending on the embassy exchange rate (currently ~1,250 NGN/USD).",
            "validity": "10 years (multiple entry, up to 6 months per visit)",
            "description": (
                "The B-1/B-2 is the standard US tourist and business visitor visa for Nigerian nationals. "
                "Applications require an online DS-160 form, payment of the MRV fee, and an in-person "
                "interview at the US Embassy in Lagos. Interview wait times in Nigeria are among the "
                "longest globally — book as early as possible. Demonstrating strong ties to Nigeria is "
                "the most critical approval factor."
            ),
        },
        "documents": [
            {
                "order": 1, "name": "International Passport", "icon_category": "passport",
                "importance": "mandatory", "condition_note": "",
                "description": "Valid US-entry travel document.",
                "sample_description": "Valid for at least 6 months beyond intended stay. Bring all previous passports.",
                "official_source_url": "https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 2, "name": "DS-160 Confirmation Page", "icon_category": "other",
                "importance": "mandatory", "condition_note": "",
                "description": "Completed online nonimmigrant visa application.",
                "sample_description": "Complete at ceac.state.gov. Print the barcode confirmation page — you cannot enter the embassy without it.",
                "official_source_url": "https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 3, "name": "MRV Fee Receipt", "icon_category": "financial",
                "importance": "mandatory", "condition_note": "",
                "description": "Proof of visa application fee payment.",
                "sample_description": "$185 paid via the US Embassy Nigeria payment portal. Print the receipt.",
                "official_source_url": "https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 4, "name": "Interview Appointment Letter", "icon_category": "other",
                "importance": "mandatory", "condition_note": "",
                "description": "Confirmation of your embassy interview slot.",
                "sample_description": "Print from the US Travel Docs portal (ustraveldocs.com).",
                "official_source_url": "https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 5, "name": "Passport Photographs", "icon_category": "photo",
                "importance": "mandatory", "condition_note": "",
                "description": "US visa specification photo.",
                "sample_description": "2 colour photos, 5cm x 5cm, white background, taken within 6 months.",
                "official_source_url": "https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 6, "name": "Bank Statements", "icon_category": "financial",
                "importance": "mandatory", "condition_note": "",
                "description": "Proof of financial capacity.",
                "sample_description": "6 months of bank statements. Consular officers look for consistent balances, not just a recent lump sum.",
                "official_source_url": "https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 7, "name": "Proof of Employment / Business", "icon_category": "employment",
                "importance": "mandatory", "condition_note": "",
                "description": "Evidence of stable income and ties to Nigeria.",
                "sample_description": "Employer letter on letterhead with your position, salary, and approved leave. Self-employed: CAC certificate and business account statements.",
                "official_source_url": "https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 8, "name": "Proof of Ties to Nigeria", "icon_category": "financial",
                "importance": "conditional", "condition_note": "Highly recommended — include as many as possible.",
                "description": "Strong ties to Nigeria to show you will return.",
                "sample_description": "Property documents, marriage certificate, children's birth certificates — anything showing you have reasons to return to Nigeria.",
                "official_source_url": "https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 9, "name": "Travel Itinerary", "icon_category": "travel",
                "importance": "optional", "condition_note": "",
                "description": "Planned US activities.",
                "sample_description": "Hotel reservations and rough trip plan. Not mandatory but advisable.",
                "official_source_url": "https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 10, "name": "Invitation Letter", "icon_category": "other",
                "importance": "conditional", "condition_note": "Only if visiting a US-based host.",
                "description": "From a US-based host.",
                "sample_description": "Signed letter with host's name, address, relationship to you, and a copy of their US ID or passport.",
                "official_source_url": "https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 11, "name": "Yellow Fever Vaccination Card", "icon_category": "medical",
                "importance": "mandatory", "condition_note": "",
                "description": "Proof of yellow fever vaccination.",
                "sample_description": "Original yellow card required before departure from Nigeria.",
                "official_source_url": "https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html",
                "last_verified": "2026-06-01",
            },
        ],
    },

    {
        "country": {"name": "Canada", "code": "CAN", "flag_emoji": "🇨🇦"},
        "visa_type": {
            "name": "Canada Temporary Resident Visa (Visitor Visa)",
            "category": "tourist",
            "processing_time": "4–8 weeks",
            "fee_usd": "74.00",
            "validity": "Up to 10 years or 1 month before passport expiry (multiple entry)",
            "description": (
                "Nigerian nationals require a Temporary Resident Visa (TRV) to visit Canada for tourism, "
                "family visits, or business. Applications are submitted online through the IRCC portal. "
                "Biometrics are required and enrolled at a VFS Global centre in Nigeria. Canada assesses "
                "applications holistically — financial stability, employment, family ties, and travel history all matter."
            ),
        },
        "documents": [
            {
                "order": 1, "name": "International Passport", "icon_category": "passport",
                "importance": "mandatory", "condition_note": "",
                "description": "Valid Canadian entry travel document.",
                "sample_description": "Valid for at least 6 months beyond your intended stay. Include old passports showing travel history.",
                "official_source_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 2, "name": "Passport Photographs", "icon_category": "photo",
                "importance": "mandatory", "condition_note": "",
                "description": "IRCC-specification photos.",
                "sample_description": "2 recent photos, 35mm x 45mm, white background. Taken within last 6 months.",
                "official_source_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 3, "name": "Biometrics Enrolment", "icon_category": "other",
                "importance": "mandatory", "condition_note": "",
                "description": "Fingerprints and photo collected at VFS.",
                "sample_description": "Book and attend a biometrics appointment at VFS Lagos or Abuja after receiving the instruction letter from IRCC.",
                "official_source_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 4, "name": "Bank Statements", "icon_category": "financial",
                "importance": "mandatory", "condition_note": "",
                "description": "Proof of sufficient funds.",
                "sample_description": "6 months of personal and/or business bank statements. Recommended minimum: CAD 2,500+ equivalent. Statements must be official bank printouts.",
                "official_source_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 5, "name": "Proof of Employment / Business", "icon_category": "employment",
                "importance": "mandatory", "condition_note": "",
                "description": "Evidence of stable income and ties to Nigeria.",
                "sample_description": "Employer letter stating role, salary, and leave approval. Self-employed: CAC documents and 6 months of business account statements.",
                "official_source_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 6, "name": "Payslips", "icon_category": "financial",
                "importance": "mandatory", "condition_note": "",
                "description": "Corroboration of income.",
                "sample_description": "Last 3 months of payslips.",
                "official_source_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 7, "name": "Travel Itinerary", "icon_category": "travel",
                "importance": "mandatory", "condition_note": "",
                "description": "Planned Canadian activities.",
                "sample_description": "Hotel bookings and flight reservation (paid ticket not required).",
                "official_source_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 8, "name": "Proof of Ties to Nigeria", "icon_category": "financial",
                "importance": "mandatory", "condition_note": "",
                "description": "Reason to return after your visit.",
                "sample_description": "Property documents, marriage certificate, children's birth certificates, or lease agreement.",
                "official_source_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 9, "name": "Invitation Letter", "icon_category": "other",
                "importance": "conditional", "condition_note": "Only if staying with a Canadian host.",
                "description": "From a Canadian citizen or permanent resident.",
                "sample_description": "Letter of invitation including the host's status document (PR card or passport) and proof of address.",
                "official_source_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 10, "name": "Travel History", "icon_category": "travel",
                "importance": "optional", "condition_note": "",
                "description": "Previous international travel record.",
                "sample_description": "Copies of previously issued visas and entry stamps — especially US, UK, Schengen.",
                "official_source_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html",
                "last_verified": "2026-06-01",
            },
            {
                "order": 11, "name": "Yellow Fever Vaccination Card", "icon_category": "medical",
                "importance": "mandatory", "condition_note": "",
                "description": "Required for Nigerian travellers.",
                "sample_description": "Original yellow card issued by a certified Nigerian health centre.",
                "official_source_url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html",
                "last_verified": "2026-06-01",
            },
        ],
    },

    {
        "country": {"name": "Australia", "code": "AUS", "flag_emoji": "🇦🇺"},
        "visa_type": {
            "name": "Australia Visitor Visa (Subclass 600)",
            "category": "tourist",
            "processing_time": "4–8 weeks",
            "fee_usd": "95.00",
            "validity": "3, 6, or 12 months (single or multiple entry)",
            "description": (
                "Nigerian nationals must apply for a Subclass 600 Visitor Visa to enter Australia for "
                "tourism or family visits. Applications are lodged online via the ImmiAccount portal. "
                "Australia requires strong proof of financial capacity and genuine intent to return to "
                "Nigeria. Health insurance and a clear itinerary significantly help the application."
            ),
        },
        "documents": [
            {
                "order": 1, "name": "International Passport", "icon_category": "passport",
                "importance": "mandatory", "condition_note": "",
                "description": "Valid Australian entry travel document.",
                "sample_description": "Valid for at least 6 months beyond intended stay. Scan the bio-data page clearly.",
                "official_source_url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-finder",
                "last_verified": "2026-06-01",
            },
            {
                "order": 2, "name": "Completed ImmiAccount Application", "icon_category": "other",
                "importance": "mandatory", "condition_note": "",
                "description": "Online visa application via immi.homeaffairs.gov.au.",
                "sample_description": "Create an ImmiAccount, complete the Subclass 600 form, and upload all documents digitally. No paper submission.",
                "official_source_url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-finder",
                "last_verified": "2026-06-01",
            },
            {
                "order": 3, "name": "Passport Photographs", "icon_category": "photo",
                "importance": "mandatory", "condition_note": "",
                "description": "Recent colour photograph.",
                "sample_description": "1 recent photo: white background, 35mm x 45mm, taken within 6 months.",
                "official_source_url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-finder",
                "last_verified": "2026-06-01",
            },
            {
                "order": 4, "name": "Bank Statements", "icon_category": "financial",
                "importance": "mandatory", "condition_note": "",
                "description": "Proof of financial capacity.",
                "sample_description": "6 months of bank statements showing sufficient funds. Recommend AUD 3,000+ equivalent. Must be on bank letterhead or official portal printout.",
                "official_source_url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-finder",
                "last_verified": "2026-06-01",
            },
            {
                "order": 5, "name": "Proof of Employment", "icon_category": "employment",
                "importance": "mandatory", "condition_note": "",
                "description": "Evidence of stable employment and ties to Nigeria.",
                "sample_description": "Employer letter on letterhead with role, salary, and confirmed leave dates.",
                "official_source_url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-finder",
                "last_verified": "2026-06-01",
            },
            {
                "order": 6, "name": "Payslips", "icon_category": "financial",
                "importance": "mandatory", "condition_note": "",
                "description": "Corroboration of employment income.",
                "sample_description": "Last 3–6 months of payslips.",
                "official_source_url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-finder",
                "last_verified": "2026-06-01",
            },
            {
                "order": 7, "name": "Travel Itinerary", "icon_category": "travel",
                "importance": "mandatory", "condition_note": "",
                "description": "Planned Australia activities.",
                "sample_description": "Flight booking confirmation and hotel reservations for the full trip duration.",
                "official_source_url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-finder",
                "last_verified": "2026-06-01",
            },
            {
                "order": 8, "name": "Proof of Ties to Nigeria", "icon_category": "financial",
                "importance": "mandatory", "condition_note": "",
                "description": "Reason to return after your visit.",
                "sample_description": "Property documents, marriage certificate, children's birth certificates, or tenancy agreement.",
                "official_source_url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-finder",
                "last_verified": "2026-06-01",
            },
            {
                "order": 9, "name": "Travel Insurance", "icon_category": "medical",
                "importance": "optional", "condition_note": "",
                "description": "Recommended travel health coverage.",
                "sample_description": "Travel insurance policy covering the entire trip. Not mandatory but strongly recommended by the Australian Department of Home Affairs.",
                "official_source_url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-finder",
                "last_verified": "2026-06-01",
            },
            {
                "order": 10, "name": "Invitation / Sponsorship Letter", "icon_category": "other",
                "importance": "conditional", "condition_note": "Only if visiting a host or sponsor in Australia.",
                "description": "From an Australian host or sponsor.",
                "sample_description": "Signed invitation letter with the sponsor's Australian residency proof and address.",
                "official_source_url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-finder",
                "last_verified": "2026-06-01",
            },
            {
                "order": 11, "name": "Travel History", "icon_category": "travel",
                "importance": "optional", "condition_note": "",
                "description": "Prior international travel record.",
                "sample_description": "Copies of previously issued visas (US, UK, Schengen) and entry/exit stamps.",
                "official_source_url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-finder",
                "last_verified": "2026-06-01",
            },
            {
                "order": 12, "name": "Yellow Fever Vaccination Card", "icon_category": "medical",
                "importance": "mandatory", "condition_note": "",
                "description": "Required for Nigerian travellers.",
                "sample_description": "Original yellow card.",
                "official_source_url": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-finder",
                "last_verified": "2026-06-01",
            },
        ],
    },

    {
        "country": {"name": "Ireland", "code": "IRL", "flag_emoji": "🇮🇪"},
        "visa_type": {
            "name": "Ireland Short Stay Visa (Type C)",
            "category": "tourist",
            "processing_time": "6–8 weeks",
            "fee_usd": "60.00",
            "validity": "90 days (single or multiple entry)",
            "description": (
                "Nigerian nationals require a Short Stay (Type C) visa to visit Ireland for tourism or "
                "family visits. Ireland is not part of the Schengen Area — a Schengen visa does not cover "
                "Ireland. Applications are submitted through the INIS online portal and processed at the "
                "Irish Embassy in Abuja or via VFS Global in Lagos."
            ),
        },
        "documents": [
            {
                "order": 1, "name": "International Passport", "icon_category": "passport",
                "importance": "mandatory", "condition_note": "",
                "description": "Valid Irish entry travel document.",
                "sample_description": "Valid for at least 12 months beyond intended date of travel. Include all previous passports.",
                "official_source_url": "https://www.irishimmigration.ie/coming-to-visit-ireland/",
                "last_verified": "2026-06-01",
            },
            {
                "order": 2, "name": "Completed AVATS Application", "icon_category": "other",
                "importance": "mandatory", "condition_note": "",
                "description": "Online Irish visa application form.",
                "sample_description": "Complete at inis.gov.ie via the AVATS online system. Print and sign the summary application form.",
                "official_source_url": "https://www.irishimmigration.ie/coming-to-visit-ireland/",
                "last_verified": "2026-06-01",
            },
            {
                "order": 3, "name": "Passport Photographs", "icon_category": "photo",
                "importance": "mandatory", "condition_note": "",
                "description": "Irish visa specification photos.",
                "sample_description": "2 recent passport photographs, white background, taken within 6 months.",
                "official_source_url": "https://www.irishimmigration.ie/coming-to-visit-ireland/",
                "last_verified": "2026-06-01",
            },
            {
                "order": 4, "name": "Bank Statements", "icon_category": "financial",
                "importance": "mandatory", "condition_note": "",
                "description": "Proof of financial capacity.",
                "sample_description": "6 months of personal bank statements. Must show sufficient funds to cover accommodation, transport, and daily expenses for the trip duration.",
                "official_source_url": "https://www.irishimmigration.ie/coming-to-visit-ireland/",
                "last_verified": "2026-06-01",
            },
            {
                "order": 5, "name": "Proof of Employment", "icon_category": "employment",
                "importance": "mandatory", "condition_note": "",
                "description": "Evidence of stable employment in Nigeria.",
                "sample_description": "Employer letter on company letterhead: role, salary, duration of employment, and approved leave.",
                "official_source_url": "https://www.irishimmigration.ie/coming-to-visit-ireland/",
                "last_verified": "2026-06-01",
            },
            {
                "order": 6, "name": "Payslips", "icon_category": "financial",
                "importance": "mandatory", "condition_note": "",
                "description": "Income corroboration.",
                "sample_description": "Last 3–6 months of payslips.",
                "official_source_url": "https://www.irishimmigration.ie/coming-to-visit-ireland/",
                "last_verified": "2026-06-01",
            },
            {
                "order": 7, "name": "Travel Itinerary", "icon_category": "travel",
                "importance": "mandatory", "condition_note": "",
                "description": "Planned Irish trip details.",
                "sample_description": "Return flight booking and hotel reservations for the full stay.",
                "official_source_url": "https://www.irishimmigration.ie/coming-to-visit-ireland/",
                "last_verified": "2026-06-01",
            },
            {
                "order": 8, "name": "Accommodation Proof", "icon_category": "accommodation",
                "importance": "mandatory", "condition_note": "",
                "description": "Where you will stay in Ireland.",
                "sample_description": "Hotel booking confirmation, or invitation letter from host plus their proof of Irish residency.",
                "official_source_url": "https://www.irishimmigration.ie/coming-to-visit-ireland/",
                "last_verified": "2026-06-01",
            },
            {
                "order": 9, "name": "Proof of Ties to Nigeria", "icon_category": "financial",
                "importance": "mandatory", "condition_note": "",
                "description": "Reason to return to Nigeria after the visit.",
                "sample_description": "Property title, tenancy agreement, birth certificates of dependants, marriage certificate.",
                "official_source_url": "https://www.irishimmigration.ie/coming-to-visit-ireland/",
                "last_verified": "2026-06-01",
            },
            {
                "order": 10, "name": "Invitation Letter", "icon_category": "other",
                "importance": "conditional", "condition_note": "Only if staying with an Ireland-based host.",
                "description": "From an Ireland-based host.",
                "sample_description": "Signed letter from host plus copy of their Irish passport or Stamp 4/Stamp 1 residence permit and a utility bill.",
                "official_source_url": "https://www.irishimmigration.ie/coming-to-visit-ireland/",
                "last_verified": "2026-06-01",
            },
            {
                "order": 11, "name": "Travel Insurance", "icon_category": "medical",
                "importance": "mandatory", "condition_note": "",
                "description": "Medical and travel coverage for Ireland.",
                "sample_description": "Policy valid for the full stay, minimum €30,000 medical coverage. Must cover Ireland specifically.",
                "official_source_url": "https://www.irishimmigration.ie/coming-to-visit-ireland/",
                "last_verified": "2026-06-01",
            },
            {
                "order": 12, "name": "Yellow Fever Vaccination Card", "icon_category": "medical",
                "importance": "mandatory", "condition_note": "",
                "description": "Required for travellers from Nigeria.",
                "sample_description": "Original yellow card.",
                "official_source_url": "https://www.irishimmigration.ie/coming-to-visit-ireland/",
                "last_verified": "2026-06-01",
            },
        ],
    },

    # =========================================================================
    # GROUP 2: SCHENGEN EUROPE (15 countries, shared Schengen checklist)
    # =========================================================================

    {
        "country": {"name": "Germany", "code": "DEU", "flag_emoji": "🇩🇪"},
        "visa_type": {
            "name": "Germany Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Nigerian nationals apply for a Schengen Type C visa at the German Embassy in Abuja or "
                "via VFS Global in Lagos. Germany is the recommended Schengen entry point when it is "
                "the main destination. The application requires an in-person appointment. Travel insurance "
                "with a minimum €30,000 cover is mandatory. Strong financial evidence and a detailed "
                "itinerary are key approval factors."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 3 months beyond your return date. Must have at least 2 blank pages. Include all previous passports.", "official_source_url": "https://nigeria.diplo.de/ng-en/service/visa", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen application form.", "sample_description": "Download from the embassy website, complete in block capitals, sign, and date. One form per applicant.", "official_source_url": "https://nigeria.diplo.de/ng-en/service/visa", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 recent biometric photos, 35mm x 45mm, white background, taken within 6 months.", "official_source_url": "https://nigeria.diplo.de/ng-en/service/visa", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen travel insurance.", "sample_description": "Policy covering all Schengen countries for the full trip duration. Minimum €30,000 medical and repatriation cover. Must be from an approved insurer.", "official_source_url": "https://nigeria.diplo.de/ng-en/service/visa", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip flight reservation showing entry and exit from the Schengen area. A booking reference is sufficient — paid ticket not always required.", "official_source_url": "https://nigeria.diplo.de/ng-en/service/visa", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel booking confirmation for the entire stay, or invitation letter from a German host with their registration certificate (Meldebescheinigung) and copy of ID.", "official_source_url": "https://nigeria.diplo.de/ng-en/service/visa", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of personal bank statements. Recommended minimum: €50–€70 per day of stay. Must be stamped and signed by your bank.", "official_source_url": "https://nigeria.diplo.de/ng-en/service/visa", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties to Nigeria.", "sample_description": "Employer letter on letterhead confirming your role, salary, and approved leave. Self-employed: CAC certificate and 6 months of business bank statements.", "official_source_url": "https://nigeria.diplo.de/ng-en/service/visa", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://nigeria.diplo.de/ng-en/service/visa", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Proof of Ties to Nigeria", "icon_category": "financial", "importance": "conditional", "condition_note": "Highly recommended.", "description": "Evidence you will return to Nigeria.", "sample_description": "Property deed, tenancy agreement, marriage certificate, children's birth certificates.", "official_source_url": "https://nigeria.diplo.de/ng-en/service/visa", "last_verified": "2026-06-01"},
            {"order": 11, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://nigeria.diplo.de/ng-en/service/visa", "last_verified": "2026-06-01"},
            {"order": 12, "name": "Invitation Letter", "icon_category": "other", "importance": "conditional", "condition_note": "Only if visiting a host in Germany.", "description": "From a Germany-based host.", "sample_description": "Formal invitation (Verpflichtungserklärung) signed at the local German Ausländerbehörde, or a personal invitation letter with host's ID and address proof.", "official_source_url": "https://nigeria.diplo.de/ng-en/service/visa", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "France", "code": "FRA", "flag_emoji": "🇫🇷"},
        "visa_type": {
            "name": "France Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Nigerian nationals apply for a French Schengen visa through the French Embassy in Abuja "
                "or via TLScontact in Lagos. Applications require an in-person biometrics appointment. "
                "France is the most visited Schengen country and a popular destination for Nigerians. "
                "A detailed itinerary, proof of funds, and travel insurance are all required."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 3 months beyond return date. Minimum 2 blank pages. Include previous passports.", "official_source_url": "https://nigeria.diplomatie.gouv.fr/en/coming-to-france/visas/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen application form.", "sample_description": "Available at TLScontact portal or France-Visas website. Complete, sign, and bring 2 copies.", "official_source_url": "https://nigeria.diplomatie.gouv.fr/en/coming-to-france/visas/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 recent biometric photos, 35mm x 45mm, white background, taken within 6 months.", "official_source_url": "https://nigeria.diplomatie.gouv.fr/en/coming-to-france/visas/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen travel insurance.", "sample_description": "Policy covering all Schengen countries for full trip. Minimum €30,000 cover. Print the certificate.", "official_source_url": "https://nigeria.diplomatie.gouv.fr/en/coming-to-france/visas/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip booking confirmation with dates and flight numbers.", "official_source_url": "https://nigeria.diplomatie.gouv.fr/en/coming-to-france/visas/", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in France.", "sample_description": "Hotel booking for entire stay, or a signed invitation letter (attestation d'accueil) from a French host, stamped by their local mairie.", "official_source_url": "https://nigeria.diplomatie.gouv.fr/en/coming-to-france/visas/", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of personal bank statements, stamped by the bank. Recommended €50–€70 per day of stay.", "official_source_url": "https://nigeria.diplomatie.gouv.fr/en/coming-to-france/visas/", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties to Nigeria.", "sample_description": "Employer letter with role, salary, leave approval. Self-employed: CAC certificate plus 6 months of business bank statements.", "official_source_url": "https://nigeria.diplomatie.gouv.fr/en/coming-to-france/visas/", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://nigeria.diplomatie.gouv.fr/en/coming-to-france/visas/", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Proof of Ties to Nigeria", "icon_category": "financial", "importance": "conditional", "condition_note": "Highly recommended.", "description": "Evidence you will return to Nigeria.", "sample_description": "Property deed, tenancy agreement, marriage/birth certificates.", "official_source_url": "https://nigeria.diplomatie.gouv.fr/en/coming-to-france/visas/", "last_verified": "2026-06-01"},
            {"order": 11, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://nigeria.diplomatie.gouv.fr/en/coming-to-france/visas/", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Italy", "code": "ITA", "flag_emoji": "🇮🇹"},
        "visa_type": {
            "name": "Italy Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Nigerian nationals apply for an Italian Schengen visa through the Italian Embassy in Abuja "
                "or via VFS Global in Lagos. Italy is the correct consulate to apply through when it is "
                "the main destination or longest stay. The application is fully in-person with biometrics."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid at least 3 months after return date. At least 2 blank pages. Include old passports.", "official_source_url": "https://vistoperitalia.esteri.it/home/en", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen application form.", "sample_description": "Download and complete the unified Schengen application form. Sign and date. One per applicant.", "official_source_url": "https://vistoperitalia.esteri.it/home/en", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 biometric photos, 35mm x 45mm, white background, within 6 months.", "official_source_url": "https://vistoperitalia.esteri.it/home/en", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen travel insurance.", "sample_description": "Minimum €30,000 coverage for medical emergencies and repatriation. Valid for all Schengen countries for the full stay.", "official_source_url": "https://vistoperitalia.esteri.it/home/en", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip booking confirmation. Paid ticket not mandatory at application stage.", "official_source_url": "https://vistoperitalia.esteri.it/home/en", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel booking for entire stay or signed host invitation with host's ID and address proof.", "official_source_url": "https://vistoperitalia.esteri.it/home/en", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of personal bank statements stamped by the bank. Recommended €50–€70 per day.", "official_source_url": "https://vistoperitalia.esteri.it/home/en", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties.", "sample_description": "Employer letter on letterhead with role, salary, leave approval. Self-employed: CAC certificate and business bank statements.", "official_source_url": "https://vistoperitalia.esteri.it/home/en", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://vistoperitalia.esteri.it/home/en", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Proof of Ties to Nigeria", "icon_category": "financial", "importance": "conditional", "condition_note": "Highly recommended.", "description": "Evidence you will return.", "sample_description": "Property deed, tenancy agreement, marriage/birth certificates.", "official_source_url": "https://vistoperitalia.esteri.it/home/en", "last_verified": "2026-06-01"},
            {"order": 11, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://vistoperitalia.esteri.it/home/en", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Spain", "code": "ESP", "flag_emoji": "🇪🇸"},
        "visa_type": {
            "name": "Spain Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Nigerian nationals apply through the Spanish Embassy in Abuja or BLS International in Lagos. "
                "Spain requires a detailed day-by-day itinerary and accommodation bookings for the full trip. "
                "Applications must be submitted in person with biometrics."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid at least 3 months after return date. Minimum 2 blank pages. Include previous passports.", "official_source_url": "https://www.exteriores.gob.es/Embajadas/abuja/en/Paginas/index.aspx", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen application form.", "sample_description": "Complete the unified Schengen form. Print, sign, and date. Submit in person at BLS or the embassy.", "official_source_url": "https://www.exteriores.gob.es/Embajadas/abuja/en/Paginas/index.aspx", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 biometric photos, 35mm x 45mm, white background, within 6 months.", "official_source_url": "https://www.exteriores.gob.es/Embajadas/abuja/en/Paginas/index.aspx", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen travel insurance.", "sample_description": "Min €30,000 medical cover for full trip. Valid for all Schengen countries.", "official_source_url": "https://www.exteriores.gob.es/Embajadas/abuja/en/Paginas/index.aspx", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip booking confirmation showing entry and exit.", "official_source_url": "https://www.exteriores.gob.es/Embajadas/abuja/en/Paginas/index.aspx", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel booking for every night of the stay. Spain requires night-by-night coverage.", "official_source_url": "https://www.exteriores.gob.es/Embajadas/abuja/en/Paginas/index.aspx", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of bank statements stamped by the bank. Minimum €65 per day or €537 per trip.", "official_source_url": "https://www.exteriores.gob.es/Embajadas/abuja/en/Paginas/index.aspx", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties.", "sample_description": "Employer letter on letterhead with role, salary, leave approval. Self-employed: CAC certificate and business bank statements.", "official_source_url": "https://www.exteriores.gob.es/Embajadas/abuja/en/Paginas/index.aspx", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://www.exteriores.gob.es/Embajadas/abuja/en/Paginas/index.aspx", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Proof of Ties to Nigeria", "icon_category": "financial", "importance": "conditional", "condition_note": "Highly recommended.", "description": "Evidence you will return.", "sample_description": "Property deed, tenancy agreement, marriage/birth certificates.", "official_source_url": "https://www.exteriores.gob.es/Embajadas/abuja/en/Paginas/index.aspx", "last_verified": "2026-06-01"},
            {"order": 11, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.exteriores.gob.es/Embajadas/abuja/en/Paginas/index.aspx", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Netherlands", "code": "NLD", "flag_emoji": "🇳🇱"},
        "visa_type": {
            "name": "Netherlands Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Nigerian nationals apply through VFS Global in Lagos or the Dutch Embassy in Abuja. "
                "The Netherlands processes applications efficiently. Biometrics are required. "
                "Strong financial evidence, travel insurance, and return flight are mandatory."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid at least 3 months after return date. Minimum 2 blank pages. Include previous passports.", "official_source_url": "https://www.netherlandsandyou.nl/your-country-and-the-netherlands/nigeria/visas-and-travel/schengen-visa", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen form.", "sample_description": "Download the unified Schengen application form, complete in full, sign and date.", "official_source_url": "https://www.netherlandsandyou.nl/your-country-and-the-netherlands/nigeria/visas-and-travel/schengen-visa", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 biometric photos, 35mm x 45mm, white background, within 6 months.", "official_source_url": "https://www.netherlandsandyou.nl/your-country-and-the-netherlands/nigeria/visas-and-travel/schengen-visa", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen insurance.", "sample_description": "Min €30,000 medical and repatriation cover for full trip duration.", "official_source_url": "https://www.netherlandsandyou.nl/your-country-and-the-netherlands/nigeria/visas-and-travel/schengen-visa", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip booking showing entry and exit from the Schengen area.", "official_source_url": "https://www.netherlandsandyou.nl/your-country-and-the-netherlands/nigeria/visas-and-travel/schengen-visa", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel booking for full stay or host invitation letter with host's address proof and ID.", "official_source_url": "https://www.netherlandsandyou.nl/your-country-and-the-netherlands/nigeria/visas-and-travel/schengen-visa", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months stamped by the bank. Recommended €34 per day minimum per Dutch guidelines.", "official_source_url": "https://www.netherlandsandyou.nl/your-country-and-the-netherlands/nigeria/visas-and-travel/schengen-visa", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties.", "sample_description": "Employer letter confirming role, salary, leave. Self-employed: CAC and business statements.", "official_source_url": "https://www.netherlandsandyou.nl/your-country-and-the-netherlands/nigeria/visas-and-travel/schengen-visa", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://www.netherlandsandyou.nl/your-country-and-the-netherlands/nigeria/visas-and-travel/schengen-visa", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.netherlandsandyou.nl/your-country-and-the-netherlands/nigeria/visas-and-travel/schengen-visa", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Belgium", "code": "BEL", "flag_emoji": "🇧🇪"},
        "visa_type": {
            "name": "Belgium Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Nigerian nationals apply through the Belgian Embassy in Abuja or VFS Global in Lagos. "
                "Belgium processes Schengen visas and requires a biometrics appointment. "
                "Comprehensive financial documentation and travel insurance are mandatory."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid at least 3 months after return. Minimum 2 blank pages. Include old passports.", "official_source_url": "https://nigeria.diplomatie.belgium.be/en/visa", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen form.", "sample_description": "Complete, sign and date the unified Schengen application form. One per applicant.", "official_source_url": "https://nigeria.diplomatie.belgium.be/en/visa", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 biometric photos, 35mm x 45mm, white background, within 6 months.", "official_source_url": "https://nigeria.diplomatie.belgium.be/en/visa", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen insurance.", "sample_description": "Min €30,000 medical cover, valid for all Schengen countries for the full trip.", "official_source_url": "https://nigeria.diplomatie.belgium.be/en/visa", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip booking confirmation.", "official_source_url": "https://nigeria.diplomatie.belgium.be/en/visa", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel booking or host invitation letter with proof of residency.", "official_source_url": "https://nigeria.diplomatie.belgium.be/en/visa", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of bank statements stamped by the bank.", "official_source_url": "https://nigeria.diplomatie.belgium.be/en/visa", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties.", "sample_description": "Employer letter on letterhead. Self-employed: CAC and business bank statements.", "official_source_url": "https://nigeria.diplomatie.belgium.be/en/visa", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://nigeria.diplomatie.belgium.be/en/visa", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://nigeria.diplomatie.belgium.be/en/visa", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Portugal", "code": "PRT", "flag_emoji": "🇵🇹"},
        "visa_type": {
            "name": "Portugal Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Nigerian nationals apply through the Portuguese Embassy in Abuja or VFS Global in Lagos. "
                "Portugal is a popular Schengen destination. Applications are in-person with biometrics. "
                "Travel insurance, return flight, and full accommodation bookings are required."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid at least 3 months after return date, minimum 2 blank pages.", "official_source_url": "https://www.vistos.mne.gov.pt/en/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen form.", "sample_description": "Complete the unified Schengen form, print, sign and date.", "official_source_url": "https://www.vistos.mne.gov.pt/en/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 biometric photos, 35mm x 45mm, white background, within 6 months.", "official_source_url": "https://www.vistos.mne.gov.pt/en/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen insurance.", "sample_description": "Min €30,000 cover for full trip, valid all Schengen countries.", "official_source_url": "https://www.vistos.mne.gov.pt/en/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip reservation showing entry and exit from Schengen area.", "official_source_url": "https://www.vistos.mne.gov.pt/en/", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel booking for full stay or signed host invitation letter with residency proof.", "official_source_url": "https://www.vistos.mne.gov.pt/en/", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of stamped personal bank statements. Minimum €40 per day recommended.", "official_source_url": "https://www.vistos.mne.gov.pt/en/", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties.", "sample_description": "Employer letter with role, salary, leave. Self-employed: CAC and business statements.", "official_source_url": "https://www.vistos.mne.gov.pt/en/", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://www.vistos.mne.gov.pt/en/", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.vistos.mne.gov.pt/en/", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Switzerland", "code": "CHE", "flag_emoji": "🇨🇭"},
        "visa_type": {
            "name": "Switzerland Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Swiss Schengen visas are processed through the Swiss Embassy in Abuja or VFS Global in Lagos. "
                "Switzerland is not an EU member but is part of the Schengen Area. "
                "Switzerland places particular emphasis on financial sufficiency — demonstrate high balances "
                "given the country's high cost of living."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid at least 3 months beyond return date, minimum 2 blank pages.", "official_source_url": "https://www.eda.admin.ch/countries/nigeria/en/home/visa/entry-ch.html", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen form.", "sample_description": "Complete, sign and date the unified Schengen application form.", "official_source_url": "https://www.eda.admin.ch/countries/nigeria/en/home/visa/entry-ch.html", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 biometric photos, 35mm x 45mm, white background, within 6 months.", "official_source_url": "https://www.eda.admin.ch/countries/nigeria/en/home/visa/entry-ch.html", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen insurance.", "sample_description": "Min €30,000 medical cover valid for all Schengen countries for full trip.", "official_source_url": "https://www.eda.admin.ch/countries/nigeria/en/home/visa/entry-ch.html", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip booking showing entry and exit from Schengen area.", "official_source_url": "https://www.eda.admin.ch/countries/nigeria/en/home/visa/entry-ch.html", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel booking or host invitation with residency proof.", "official_source_url": "https://www.eda.admin.ch/countries/nigeria/en/home/visa/entry-ch.html", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of substantial financial means.", "sample_description": "6 months of bank statements. Switzerland is expensive — recommend demonstrating CHF 100+ per day. Statements must be stamped by the bank.", "official_source_url": "https://www.eda.admin.ch/countries/nigeria/en/home/visa/entry-ch.html", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties.", "sample_description": "Employer letter on letterhead. Self-employed: CAC certificate and business bank statements.", "official_source_url": "https://www.eda.admin.ch/countries/nigeria/en/home/visa/entry-ch.html", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://www.eda.admin.ch/countries/nigeria/en/home/visa/entry-ch.html", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.eda.admin.ch/countries/nigeria/en/home/visa/entry-ch.html", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Austria", "code": "AUT", "flag_emoji": "🇦🇹"},
        "visa_type": {
            "name": "Austria Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Austrian Schengen visas are processed through the Austrian Embassy in Abuja or VFS Global in Lagos. "
                "Austria requires a detailed itinerary and all standard Schengen documents. "
                "Biometrics enrolment is mandatory."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid at least 3 months after return date. Minimum 2 blank pages.", "official_source_url": "https://www.bmeia.gv.at/en/austrian-embassy/abuja/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen form.", "sample_description": "Complete the unified Schengen form, print, sign and date.", "official_source_url": "https://www.bmeia.gv.at/en/austrian-embassy/abuja/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 biometric photos, 35mm x 45mm, white background, within 6 months.", "official_source_url": "https://www.bmeia.gv.at/en/austrian-embassy/abuja/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen insurance.", "sample_description": "Min €30,000 medical and repatriation cover for full trip.", "official_source_url": "https://www.bmeia.gv.at/en/austrian-embassy/abuja/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip booking showing entry and exit.", "official_source_url": "https://www.bmeia.gv.at/en/austrian-embassy/abuja/", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel booking for full stay or host invitation with residency proof.", "official_source_url": "https://www.bmeia.gv.at/en/austrian-embassy/abuja/", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of stamped bank statements. Recommend €50–€70 per day of stay.", "official_source_url": "https://www.bmeia.gv.at/en/austrian-embassy/abuja/", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties.", "sample_description": "Employer letter on letterhead. Self-employed: CAC and business statements.", "official_source_url": "https://www.bmeia.gv.at/en/austrian-embassy/abuja/", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://www.bmeia.gv.at/en/austrian-embassy/abuja/", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.bmeia.gv.at/en/austrian-embassy/abuja/", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Sweden", "code": "SWE", "flag_emoji": "🇸🇪"},
        "visa_type": {
            "name": "Sweden Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Nigerian nationals apply through the Swedish Embassy in Abuja or VFS Global in Lagos. "
                "Sweden is a Schengen member state. Standard Schengen documentation applies. "
                "Sweden is strict about genuine tourist intent and ties to Nigeria."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid at least 3 months after return. Minimum 2 blank pages. Include old passports.", "official_source_url": "https://www.swedenabroad.se/en/embassies/nigeria-abuja/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen form.", "sample_description": "Complete the unified Schengen application form, sign and date.", "official_source_url": "https://www.swedenabroad.se/en/embassies/nigeria-abuja/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 biometric photos, 35mm x 45mm, white background, within 6 months.", "official_source_url": "https://www.swedenabroad.se/en/embassies/nigeria-abuja/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen insurance.", "sample_description": "Min €30,000 medical cover for full trip, all Schengen countries.", "official_source_url": "https://www.swedenabroad.se/en/embassies/nigeria-abuja/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip booking confirmation with dates and flight numbers.", "official_source_url": "https://www.swedenabroad.se/en/embassies/nigeria-abuja/", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel booking for full stay or signed host invitation with ID and address proof.", "official_source_url": "https://www.swedenabroad.se/en/embassies/nigeria-abuja/", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of stamped bank statements. Recommend SEK 450+ per day equivalent.", "official_source_url": "https://www.swedenabroad.se/en/embassies/nigeria-abuja/", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties.", "sample_description": "Employer letter on letterhead with role, salary, leave approval. Self-employed: CAC and business statements.", "official_source_url": "https://www.swedenabroad.se/en/embassies/nigeria-abuja/", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://www.swedenabroad.se/en/embassies/nigeria-abuja/", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.swedenabroad.se/en/embassies/nigeria-abuja/", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Norway", "code": "NOR", "flag_emoji": "🇳🇴"},
        "visa_type": {
            "name": "Norway Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Norway is a Schengen member (not EU). Nigerian nationals apply through VFS Global in Lagos. "
                "Norway processes applications quickly but is strict about financial sufficiency given the "
                "country's high cost of living. Standard Schengen document requirements apply."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid at least 3 months after return date. Minimum 2 blank pages.", "official_source_url": "https://www.norway.no/en/nigeria/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen form.", "sample_description": "Complete the unified Schengen form, sign and date it.", "official_source_url": "https://www.norway.no/en/nigeria/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 biometric photos, 35mm x 45mm, white background, within 6 months.", "official_source_url": "https://www.norway.no/en/nigeria/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen insurance.", "sample_description": "Min €30,000 medical and repatriation cover for the full trip.", "official_source_url": "https://www.norway.no/en/nigeria/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip reservation showing entry and exit.", "official_source_url": "https://www.norway.no/en/nigeria/", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel booking for entire stay or host invitation with residency proof.", "official_source_url": "https://www.norway.no/en/nigeria/", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of substantial financial means.", "sample_description": "6 months of stamped bank statements. Norway is expensive — recommend NOK 500+ per day equivalent.", "official_source_url": "https://www.norway.no/en/nigeria/", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties.", "sample_description": "Employer letter on letterhead. Self-employed: CAC and business statements.", "official_source_url": "https://www.norway.no/en/nigeria/", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://www.norway.no/en/nigeria/", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.norway.no/en/nigeria/", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Denmark", "code": "DNK", "flag_emoji": "🇩🇰"},
        "visa_type": {
            "name": "Denmark Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Nigerian nationals apply through the Danish Embassy in Abuja or VFS Global in Lagos. "
                "Denmark is a Schengen member. Standard Schengen checklist applies. "
                "Applications must be submitted in person with biometrics."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid at least 3 months after return. Minimum 2 blank pages.", "official_source_url": "https://nigeria.um.dk/en/travel-and-residence/visas", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen form.", "sample_description": "Complete the unified form, sign and date.", "official_source_url": "https://nigeria.um.dk/en/travel-and-residence/visas", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 biometric photos, 35mm x 45mm, white background, within 6 months.", "official_source_url": "https://nigeria.um.dk/en/travel-and-residence/visas", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen insurance.", "sample_description": "Min €30,000 medical cover for full trip, valid in all Schengen countries.", "official_source_url": "https://nigeria.um.dk/en/travel-and-residence/visas", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip booking showing entry and exit.", "official_source_url": "https://nigeria.um.dk/en/travel-and-residence/visas", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel booking for full stay or host invitation with residency proof.", "official_source_url": "https://nigeria.um.dk/en/travel-and-residence/visas", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of stamped bank statements.", "official_source_url": "https://nigeria.um.dk/en/travel-and-residence/visas", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties.", "sample_description": "Employer letter on letterhead. Self-employed: CAC and business bank statements.", "official_source_url": "https://nigeria.um.dk/en/travel-and-residence/visas", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://nigeria.um.dk/en/travel-and-residence/visas", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://nigeria.um.dk/en/travel-and-residence/visas", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Greece", "code": "GRC", "flag_emoji": "🇬🇷"},
        "visa_type": {
            "name": "Greece Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Nigerian nationals apply through the Greek Embassy in Abuja or VFS Global in Lagos. "
                "Greece is a Schengen member and a popular tourist destination. "
                "All standard Schengen requirements apply. A detailed itinerary for island or mainland "
                "travel significantly strengthens the application."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid at least 3 months after return. Minimum 2 blank pages.", "official_source_url": "https://www.mfa.gr/en/visas/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen form.", "sample_description": "Complete the unified Schengen form, sign and date.", "official_source_url": "https://www.mfa.gr/en/visas/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 biometric photos, 35mm x 45mm, white background, within 6 months.", "official_source_url": "https://www.mfa.gr/en/visas/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen insurance.", "sample_description": "Min €30,000 medical cover for full trip, valid in all Schengen countries.", "official_source_url": "https://www.mfa.gr/en/visas/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip booking showing entry and exit.", "official_source_url": "https://www.mfa.gr/en/visas/", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel booking for full stay or host invitation with residency proof.", "official_source_url": "https://www.mfa.gr/en/visas/", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of stamped bank statements. Greece requires minimum €50 per day.", "official_source_url": "https://www.mfa.gr/en/visas/", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties.", "sample_description": "Employer letter on letterhead. Self-employed: CAC and business statements.", "official_source_url": "https://www.mfa.gr/en/visas/", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://www.mfa.gr/en/visas/", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.mfa.gr/en/visas/", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Poland", "code": "POL", "flag_emoji": "🇵🇱"},
        "visa_type": {
            "name": "Poland Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Nigerian nationals apply through the Polish Embassy in Abuja or VFS Global in Lagos. "
                "Poland is a full Schengen member. Standard Schengen requirements apply. "
                "Poland is increasingly popular for Nigerians visiting family or touring Eastern Europe."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid at least 3 months after return date. Minimum 2 blank pages.", "official_source_url": "https://www.gov.pl/web/nigeria/visa-information", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen form.", "sample_description": "Complete the unified Schengen form, sign and date.", "official_source_url": "https://www.gov.pl/web/nigeria/visa-information", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 biometric photos, 35mm x 45mm, white background, within 6 months.", "official_source_url": "https://www.gov.pl/web/nigeria/visa-information", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen insurance.", "sample_description": "Min €30,000 medical cover for full trip, valid in all Schengen countries.", "official_source_url": "https://www.gov.pl/web/nigeria/visa-information", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip booking showing entry and exit.", "official_source_url": "https://www.gov.pl/web/nigeria/visa-information", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel booking for full stay or host invitation with residency proof.", "official_source_url": "https://www.gov.pl/web/nigeria/visa-information", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of stamped bank statements.", "official_source_url": "https://www.gov.pl/web/nigeria/visa-information", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties.", "sample_description": "Employer letter on letterhead. Self-employed: CAC and business statements.", "official_source_url": "https://www.gov.pl/web/nigeria/visa-information", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://www.gov.pl/web/nigeria/visa-information", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.gov.pl/web/nigeria/visa-information", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Czech Republic", "code": "CZE", "flag_emoji": "🇨🇿"},
        "visa_type": {
            "name": "Czech Republic Schengen Visa (Type C – Tourist)",
            "category": "tourist",
            "processing_time": "2–4 weeks",
            "fee_usd": "90.00",
            "validity": "90 days within 180-day period",
            "description": (
                "Nigerian nationals apply through the Czech Embassy in Abuja or VFS Global in Lagos. "
                "Czech Republic is a Schengen member and Prague is a popular tourist destination. "
                "Standard Schengen documentation applies."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid at least 3 months after return. Minimum 2 blank pages.", "official_source_url": "https://www.mzv.cz/abuja/en/visa_and_consular_services/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Schengen Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Schengen form.", "sample_description": "Complete the unified Schengen form, sign and date.", "official_source_url": "https://www.mzv.cz/abuja/en/visa_and_consular_services/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Schengen-specification photos.", "sample_description": "2 biometric photos, 35mm x 45mm, white background, within 6 months.", "official_source_url": "https://www.mzv.cz/abuja/en/visa_and_consular_services/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Mandatory Schengen insurance.", "sample_description": "Min €30,000 medical cover for full trip, valid in all Schengen countries.", "official_source_url": "https://www.mzv.cz/abuja/en/visa_and_consular_services/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Itinerary / Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip booking showing entry and exit.", "official_source_url": "https://www.mzv.cz/abuja/en/visa_and_consular_services/", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel booking for full stay or host invitation with residency proof.", "official_source_url": "https://www.mzv.cz/abuja/en/visa_and_consular_services/", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of stamped bank statements.", "official_source_url": "https://www.mzv.cz/abuja/en/visa_and_consular_services/", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment / Business", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of economic ties.", "sample_description": "Employer letter on letterhead. Self-employed: CAC and business bank statements.", "official_source_url": "https://www.mzv.cz/abuja/en/visa_and_consular_services/", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://www.mzv.cz/abuja/en/visa_and_consular_services/", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.mzv.cz/abuja/en/visa_and_consular_services/", "last_verified": "2026-06-01"},
        ],
    },

    # =========================================================================
    # GROUP 3: ASIA-PACIFIC
    # =========================================================================

    {
        "country": {"name": "United Arab Emirates", "code": "ARE", "flag_emoji": "🇦🇪"},
        "visa_type": {
            "name": "UAE Tourist Visa",
            "category": "tourist",
            "processing_time": "3–5 business days",
            "fee_usd": "90.00",
            "validity": "30 or 60 days (single or multiple entry)",
            "description": (
                "Nigerian nationals can apply for a UAE tourist visa online via the ICP portal or through "
                "airlines such as Emirates and Etihad. The UAE is one of the most accessible destinations "
                "for Nigerians. Approval rates are generally high. Applications can also be sponsored "
                "by a hotel or tour operator. Biometrics are taken on arrival."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid UAE entry travel document.", "sample_description": "Valid for at least 6 months beyond travel date. Scanned colour copy of biodata page required for online application.", "official_source_url": "https://icp.gov.ae/en/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Passport Photograph", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Recent colour photograph.", "sample_description": "1 recent colour photo with white background. Must clearly show your face.", "official_source_url": "https://icp.gov.ae/en/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of sufficient funds.", "sample_description": "3 months of personal bank statements showing sufficient funds. Recommended AED 3,000+ equivalent balance.", "official_source_url": "https://icp.gov.ae/en/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Confirmed Return Flight Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Proof of onward/return travel.", "sample_description": "Round-trip flight booking confirmation showing entry and exit from the UAE.", "official_source_url": "https://icp.gov.ae/en/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Hotel Booking / Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in the UAE.", "sample_description": "Hotel reservation for the full stay. If staying with a host, a copy of their UAE residency visa and Emirates ID.", "official_source_url": "https://icp.gov.ae/en/", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Travel Insurance", "icon_category": "medical", "importance": "optional", "condition_note": "", "description": "Recommended health coverage.", "sample_description": "Travel insurance covering medical emergencies for the trip duration. Not mandatory but strongly recommended.", "official_source_url": "https://icp.gov.ae/en/", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card required before departure from Nigeria.", "official_source_url": "https://icp.gov.ae/en/", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Turkey", "code": "TUR", "flag_emoji": "🇹🇷"},
        "visa_type": {
            "name": "Turkey e-Visa",
            "category": "tourist",
            "processing_time": "Immediate to 24 hours (online)",
            "fee_usd": "55.00",
            "validity": "30 days per stay, multiple entry within 180 days",
            "description": (
                "Nigerian nationals can obtain a Turkey e-Visa entirely online at evisa.gov.tr. "
                "The process is quick and does not require an embassy visit. Most applicants receive "
                "approval within minutes to a few hours. The e-Visa allows tourism and short visits. "
                "No physical stamping required — the e-Visa is linked to your passport electronically."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 60 days beyond your intended stay. Biodata page scan required for e-Visa application.", "official_source_url": "https://www.evisa.gov.tr/en/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Credit/Debit Card for e-Visa Fee", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Payment for the online e-Visa.", "sample_description": "International card (Visa/Mastercard) needed to pay the $55 e-Visa fee online at evisa.gov.tr.", "official_source_url": "https://www.evisa.gov.tr/en/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Valid Email Address", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "For e-Visa delivery.", "sample_description": "Your e-Visa approval will be sent to your email. Print it and carry it when travelling.", "official_source_url": "https://www.evisa.gov.tr/en/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Return Flight Booking", "icon_category": "travel", "importance": "optional", "condition_note": "", "description": "Proof of onward travel.", "sample_description": "Round-trip flight booking. Not required for the e-Visa but may be checked at the airport or port of entry.", "official_source_url": "https://www.evisa.gov.tr/en/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Hotel Booking", "icon_category": "accommodation", "importance": "optional", "condition_note": "", "description": "Proof of accommodation.", "sample_description": "Hotel reservation. Not required for the e-Visa but may be requested on arrival.", "official_source_url": "https://www.evisa.gov.tr/en/", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.evisa.gov.tr/en/", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Japan", "code": "JPN", "flag_emoji": "🇯🇵"},
        "visa_type": {
            "name": "Japan Tourist Visa",
            "category": "tourist",
            "processing_time": "5–7 business days",
            "fee_usd": "28.00",
            "validity": "Single or double entry, up to 90 days stay",
            "description": (
                "Nigerian nationals must apply for a Japanese tourist visa through the Embassy of Japan "
                "in Abuja. Japan requires in-person application submission and is known for thorough "
                "document scrutiny. Financial documentation must be especially strong. "
                "A detailed day-by-day itinerary is a key requirement."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for the entire period of stay. Include all previous passports.", "official_source_url": "https://www.ng.emb-japan.go.jp/itpr_en/visa.html", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Japanese embassy application form.", "sample_description": "Download from the Japanese Embassy website. Complete in English, sign and date.", "official_source_url": "https://www.ng.emb-japan.go.jp/itpr_en/visa.html", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photograph", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Japan-specification photo.", "sample_description": "1 recent colour photo, 45mm x 45mm, white or light grey background, taken within 6 months. No glasses.", "official_source_url": "https://www.ng.emb-japan.go.jp/itpr_en/visa.html", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Day-by-Day Travel Itinerary", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Detailed Japan travel plan.", "sample_description": "A day-by-day schedule listing cities to visit, activities, and hotels. Japan requires this to be detailed and plausible.", "official_source_url": "https://www.ng.emb-japan.go.jp/itpr_en/visa.html", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Flight Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip flight reservation. A booking reference is acceptable.", "official_source_url": "https://www.ng.emb-japan.go.jp/itpr_en/visa.html", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in Japan.", "sample_description": "Hotel bookings for every night of the trip. Japan requires this for all nights.", "official_source_url": "https://www.ng.emb-japan.go.jp/itpr_en/visa.html", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of substantial financial means.", "sample_description": "6 months of personal bank statements. Japan expects substantial balances — recommend JPY 300,000+ equivalent minimum. Original stamped by bank.", "official_source_url": "https://www.ng.emb-japan.go.jp/itpr_en/visa.html", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Employment", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of employment and income.", "sample_description": "Employer letter on letterhead with role, salary, and approved leave. Self-employed: CAC certificate and 6 months of business statements.", "official_source_url": "https://www.ng.emb-japan.go.jp/itpr_en/visa.html", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://www.ng.emb-japan.go.jp/itpr_en/visa.html", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Proof of Ties to Nigeria", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Evidence you will return.", "sample_description": "Property deed, marriage certificate, birth certificates of dependants, tenancy agreement.", "official_source_url": "https://www.ng.emb-japan.go.jp/itpr_en/visa.html", "last_verified": "2026-06-01"},
            {"order": 11, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.ng.emb-japan.go.jp/itpr_en/visa.html", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "China", "code": "CHN", "flag_emoji": "🇨🇳"},
        "visa_type": {
            "name": "China Tourist Visa (L Visa)",
            "category": "tourist",
            "processing_time": "4–7 business days",
            "fee_usd": "140.00",
            "validity": "30–90 days (single, double, or multiple entry)",
            "description": (
                "Nigerian nationals apply for a Chinese L (tourist) visa through the Chinese Embassy in Abuja "
                "or the Consulate in Lagos. In-person submission is required. China has recently expanded "
                "its digital application system. An invitation letter from a Chinese travel agency or sponsor "
                "significantly strengthens the application."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 6 months beyond intended stay. Must have at least 2 blank visa pages.", "official_source_url": "https://www.visaforchina.cn/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "China Visa Application Form (V.2013)", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Official Chinese visa application form.", "sample_description": "Complete online at visaforchina.cn or in person. Print, sign and bring the completed form.", "official_source_url": "https://www.visaforchina.cn/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photograph", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "China visa specification photo.", "sample_description": "1 recent colour photo, 33mm x 48mm, white background, full face, taken within 6 months.", "official_source_url": "https://www.visaforchina.cn/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Round-Trip Flight Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Confirmed round-trip booking showing entry and exit from China.", "official_source_url": "https://www.visaforchina.cn/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Hotel Booking / Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in China.", "sample_description": "Hotel booking confirmation for the full stay. Chinese hotel booking must be from a registered hotel.", "official_source_url": "https://www.visaforchina.cn/", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "3–6 months of personal bank statements. Recommend CNY 5,000+ equivalent balance.", "official_source_url": "https://www.visaforchina.cn/", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Proof of Employment", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of employment.", "sample_description": "Employer letter on letterhead with role, salary, and approved leave. Self-employed: CAC certificate and business statements.", "official_source_url": "https://www.visaforchina.cn/", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Invitation Letter from Chinese Host or Travel Agency", "icon_category": "other", "importance": "conditional", "condition_note": "Strongly recommended if available.", "description": "Invitation from a Chinese host or licensed travel agency.", "sample_description": "Letter from a Chinese citizen or registered travel agency confirming your itinerary and contact details. Include host's ID or agency registration.", "official_source_url": "https://www.visaforchina.cn/", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.visaforchina.cn/", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "India", "code": "IND", "flag_emoji": "🇮🇳"},
        "visa_type": {
            "name": "India e-Tourist Visa",
            "category": "tourist",
            "processing_time": "3–5 business days",
            "fee_usd": "25.00",
            "validity": "30 days (double entry) for 30-day e-Visa; 1 year (multiple entry) for extended options",
            "description": (
                "Nigerian nationals can apply for an Indian e-Tourist Visa entirely online at indianvisaonline.gov.in. "
                "No embassy visit is required. The e-Visa is sent to your email and presented on arrival. "
                "India also offers 1-year and 5-year e-Tourist Visas at higher fees. "
                "Processing typically takes 3–5 business days."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 6 months beyond travel date. Scanned biodata page required for online application.", "official_source_url": "https://indianvisaonline.gov.in/evisa/tvoa.html", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Passport Photograph (Digital)", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Digital photo for the e-Visa form.", "sample_description": "Recent colour photo, white background, jpg format, file size 10KB–1MB. Upload during online application.", "official_source_url": "https://indianvisaonline.gov.in/evisa/tvoa.html", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Credit/Debit Card for e-Visa Fee", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Payment for the online e-Visa.", "sample_description": "International Visa/Mastercard needed to pay the e-Visa fee online.", "official_source_url": "https://indianvisaonline.gov.in/evisa/tvoa.html", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Return Flight Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Proof of onward travel.", "sample_description": "Round-trip flight confirmation. Required for the e-Visa application form.", "official_source_url": "https://indianvisaonline.gov.in/evisa/tvoa.html", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Hotel Booking", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in India.", "sample_description": "First-night hotel confirmation is required on the e-Visa form. Full itinerary recommended.", "official_source_url": "https://indianvisaonline.gov.in/evisa/tvoa.html", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Bank Statements", "icon_category": "financial", "importance": "optional", "condition_note": "", "description": "Proof of financial means.", "sample_description": "3–6 months of bank statements. Not required at application stage but may be requested at the airport on arrival.", "official_source_url": "https://indianvisaonline.gov.in/evisa/tvoa.html", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers. India strictly enforces this.", "sample_description": "Original yellow card. Travellers arriving from Nigeria without this can be refused entry.", "official_source_url": "https://indianvisaonline.gov.in/evisa/tvoa.html", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Malaysia", "code": "MYS", "flag_emoji": "🇲🇾"},
        "visa_type": {
            "name": "Malaysia eNTRI / eVisa",
            "category": "tourist",
            "processing_time": "1–3 business days",
            "fee_usd": "35.00",
            "validity": "30 days single entry",
            "description": (
                "Nigerian nationals can apply for a Malaysian eVisa online through the Malaysia Visa Online portal. "
                "Malaysia is one of the more accessible Southeast Asian destinations for Nigerian travellers. "
                "The eVisa is processed electronically and presented on arrival. "
                "No embassy appointment is needed for the eVisa."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 6 months beyond travel date. Scanned biodata page required.", "official_source_url": "https://www.windowmalaysia.my/evisa/evisa.html", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Passport Photograph (Digital)", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Digital colour photo.", "sample_description": "Recent colour photo, white background, jpg format. Upload during online application.", "official_source_url": "https://www.windowmalaysia.my/evisa/evisa.html", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Return Flight Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Proof of onward travel.", "sample_description": "Round-trip flight booking confirmation.", "official_source_url": "https://www.windowmalaysia.my/evisa/evisa.html", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Hotel Booking", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in Malaysia.", "sample_description": "Hotel booking for the full duration of stay.", "official_source_url": "https://www.windowmalaysia.my/evisa/evisa.html", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "3 months of bank statements showing sufficient funds. Recommend MYR 1,500+ equivalent.", "official_source_url": "https://www.windowmalaysia.my/evisa/evisa.html", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.windowmalaysia.my/evisa/evisa.html", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Singapore", "code": "SGP", "flag_emoji": "🇸🇬"},
        "visa_type": {
            "name": "Singapore Tourist Visa",
            "category": "tourist",
            "processing_time": "3–5 business days",
            "fee_usd": "30.00",
            "validity": "30 days single entry (up to 90 days stay granted at entry)",
            "description": (
                "Nigerian nationals require a tourist visa to enter Singapore. Applications are submitted "
                "through an authorised contact (a Singapore-based sponsor, hotel, or travel agency) who "
                "applies on the applicant's behalf through the ICA e-Service portal. "
                "Alternatively, some travel agents in Nigeria can facilitate Singapore visa applications. "
                "Strong financial evidence is essential."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 6 months beyond intended stay. Scanned biodata page required.", "official_source_url": "https://www.ica.gov.sg/enter-transit-depart/entering-singapore/visa_requirements", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Application Form (14A)", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Singapore visa application form.", "sample_description": "Form 14A completed and signed. Your Singapore-based sponsor or travel agent submits it via the ICA e-Service portal.", "official_source_url": "https://www.ica.gov.sg/enter-transit-depart/entering-singapore/visa_requirements", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photograph", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Recent colour photograph.", "sample_description": "1 recent colour photo, 35mm x 45mm, white background, taken within 3 months.", "official_source_url": "https://www.ica.gov.sg/enter-transit-depart/entering-singapore/visa_requirements", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "3–6 months of bank statements. Recommend SGD 1,500+ equivalent. Must be stamped by the bank.", "official_source_url": "https://www.ica.gov.sg/enter-transit-depart/entering-singapore/visa_requirements", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Proof of Employment", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of employment in Nigeria.", "sample_description": "Employer letter on letterhead with role, salary, leave approval. Self-employed: CAC and business statements.", "official_source_url": "https://www.ica.gov.sg/enter-transit-depart/entering-singapore/visa_requirements", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Return Flight Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Proof of onward travel.", "sample_description": "Round-trip flight booking confirmation.", "official_source_url": "https://www.ica.gov.sg/enter-transit-depart/entering-singapore/visa_requirements", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Hotel Booking", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in Singapore.", "sample_description": "Hotel booking for full stay or sponsor's contact details and address.", "official_source_url": "https://www.ica.gov.sg/enter-transit-depart/entering-singapore/visa_requirements", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Sponsor / Reference in Singapore", "icon_category": "other", "importance": "conditional", "condition_note": "Required if not applying via a travel agency.", "description": "Singapore-based sponsor or hotel reference.", "sample_description": "Name, address, and contact number of your Singapore-based sponsor (hotel or individual), along with their NRIC or work permit number.", "official_source_url": "https://www.ica.gov.sg/enter-transit-depart/entering-singapore/visa_requirements", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.ica.gov.sg/enter-transit-depart/entering-singapore/visa_requirements", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "South Korea", "code": "KOR", "flag_emoji": "🇰🇷"},
        "visa_type": {
            "name": "South Korea Tourist Visa (C-3)",
            "category": "tourist",
            "processing_time": "5–7 business days",
            "fee_usd": "40.00",
            "validity": "Single or multiple entry, up to 90 days stay",
            "description": (
                "Nigerian nationals must apply for a South Korean C-3 (short-stay) visa at the Korean "
                "Embassy in Abuja. In-person application with biometrics is required. "
                "South Korea requires thorough financial documentation and a detailed itinerary. "
                "Strong travel history to other countries improves approval chances."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 6 months beyond intended stay. Include all previous passports.", "official_source_url": "https://nga.mofa.go.kr/eng/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Korean Embassy application form.", "sample_description": "Download from the Korean Embassy website. Complete in English or Korean, print, sign and submit in person.", "official_source_url": "https://nga.mofa.go.kr/eng/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photograph", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Korea visa specification photo.", "sample_description": "1 recent colour photo, 35mm x 45mm, white background, taken within 6 months.", "official_source_url": "https://nga.mofa.go.kr/eng/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of bank statements stamped by the bank. Recommend KRW 500,000+ equivalent per week of stay.", "official_source_url": "https://nga.mofa.go.kr/eng/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Proof of Employment", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of stable employment.", "sample_description": "Employer letter on letterhead. Self-employed: CAC and business bank statements.", "official_source_url": "https://nga.mofa.go.kr/eng/", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://nga.mofa.go.kr/eng/", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Round-Trip Flight Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight booking.", "sample_description": "Round-trip flight booking confirmation.", "official_source_url": "https://nga.mofa.go.kr/eng/", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Hotel Booking", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in South Korea.", "sample_description": "Hotel booking for the full stay.", "official_source_url": "https://nga.mofa.go.kr/eng/", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Travel Itinerary", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Planned South Korea activities.", "sample_description": "Day-by-day itinerary covering cities, tourist sites, and activities.", "official_source_url": "https://nga.mofa.go.kr/eng/", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Proof of Ties to Nigeria", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Evidence you will return to Nigeria.", "sample_description": "Property deed, marriage certificate, dependants' birth certificates.", "official_source_url": "https://nga.mofa.go.kr/eng/", "last_verified": "2026-06-01"},
            {"order": 11, "name": "Travel History", "icon_category": "travel", "importance": "optional", "condition_note": "", "description": "Prior international travel.", "sample_description": "Copies of previous visas and entry/exit stamps (especially US, UK, Schengen, Japan).", "official_source_url": "https://nga.mofa.go.kr/eng/", "last_verified": "2026-06-01"},
            {"order": 12, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://nga.mofa.go.kr/eng/", "last_verified": "2026-06-01"},
        ],
    },

    # =========================================================================
    # GROUP 4: MIDDLE EAST, AFRICA & AMERICAS
    # =========================================================================

    {
        "country": {"name": "Saudi Arabia", "code": "SAU", "flag_emoji": "🇸🇦"},
        "visa_type": {
            "name": "Saudi Arabia Tourist e-Visa",
            "category": "tourist",
            "processing_time": "Immediate to 24 hours",
            "fee_usd": "125.00",
            "validity": "1 year, multiple entry, 90 days per stay",
            "description": (
                "Nigerian nationals can apply for a Saudi tourist e-Visa online at visitsaudi.com. "
                "Saudi Arabia opened its doors to international tourism in 2019 and the process is "
                "straightforward. The e-Visa is electronically linked to your passport. "
                "The fee includes mandatory medical insurance. No embassy visit is required."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 6 months beyond travel date. Scanned colour copy of biodata page required.", "official_source_url": "https://www.visitsaudi.com/en/plan/visa-information", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Passport Photograph (Digital)", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Digital colour photo.", "sample_description": "Recent colour photo, white background, uploaded during the online application.", "official_source_url": "https://www.visitsaudi.com/en/plan/visa-information", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Credit/Debit Card for e-Visa Fee", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Payment for e-Visa (includes mandatory medical insurance).", "sample_description": "International Visa/Mastercard. The $125 fee includes complimentary travel insurance for the trip.", "official_source_url": "https://www.visitsaudi.com/en/plan/visa-information", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Return Flight Booking", "icon_category": "travel", "importance": "optional", "condition_note": "", "description": "May be requested at the border.", "sample_description": "Round-trip flight booking. Not required for the online application but advisable to carry.", "official_source_url": "https://www.visitsaudi.com/en/plan/visa-information", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.visitsaudi.com/en/plan/visa-information", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Meningitis Vaccination Certificate", "icon_category": "medical", "importance": "mandatory", "condition_note": "Required if travelling to Mecca or Medina for Umrah / Hajj.", "description": "Required for pilgrimage travel.", "sample_description": "Certificate showing ACWY meningitis vaccination. Required for Hajj and Umrah visas (different from tourist e-Visa).", "official_source_url": "https://www.visitsaudi.com/en/plan/visa-information", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Qatar", "code": "QAT", "flag_emoji": "🇶🇦"},
        "visa_type": {
            "name": "Qatar Tourist Visa (Hayya / e-Visa)",
            "category": "tourist",
            "processing_time": "Immediate to 3 business days",
            "fee_usd": "17.00",
            "validity": "30 days, extendable to 90 days",
            "description": (
                "Nigerian nationals can obtain a Qatar tourist visa online through the Hayya portal or "
                "the Qatar Visa Centre. Doha is also a major transit hub for Nigerians. "
                "The visa is low cost and the application is straightforward. "
                "Qatar Airways passengers may be eligible for a free transit visa or complimentary stopover."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 6 months beyond travel date. Scanned biodata page required.", "official_source_url": "https://www.visitqatar.qa/en/plan-your-trip/know-before-you-go/visa-information", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Passport Photograph (Digital)", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Digital colour photo.", "sample_description": "Recent colour photo, white background, uploaded during the online application.", "official_source_url": "https://www.visitqatar.qa/en/plan-your-trip/know-before-you-go/visa-information", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Return Flight Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Proof of onward travel.", "sample_description": "Round-trip flight confirmation showing entry and exit from Qatar.", "official_source_url": "https://www.visitqatar.qa/en/plan-your-trip/know-before-you-go/visa-information", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Hotel Booking", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in Qatar.", "sample_description": "Hotel reservation for the full duration of stay.", "official_source_url": "https://www.visitqatar.qa/en/plan-your-trip/know-before-you-go/visa-information", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "3 months of bank statements showing sufficient funds.", "official_source_url": "https://www.visitqatar.qa/en/plan-your-trip/know-before-you-go/visa-information", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.visitqatar.qa/en/plan-your-trip/know-before-you-go/visa-information", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Kenya", "code": "KEN", "flag_emoji": "🇰🇪"},
        "visa_type": {
            "name": "Kenya e-Visa (East Africa Tourist Visa)",
            "category": "tourist",
            "processing_time": "3–5 business days",
            "fee_usd": "50.00",
            "validity": "90 days single entry (East Africa Tourist Visa covers Kenya, Uganda, Rwanda)",
            "description": (
                "Nigerian nationals can apply for a Kenyan e-Visa online at evisa.go.ke. "
                "The East Africa Tourist Visa ($100) allows travel across Kenya, Uganda, and Rwanda — "
                "excellent value for a regional safari trip. The single-country Kenya e-Visa costs $50. "
                "No embassy visit required. Approval is typically within 3–5 business days."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 6 months beyond travel date. Scanned biodata page required for online application.", "official_source_url": "https://evisa.go.ke/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Passport Photograph (Digital)", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Digital colour photo.", "sample_description": "Recent colour photo, white background, jpg format, uploaded during application.", "official_source_url": "https://evisa.go.ke/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Return Flight Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Proof of onward travel.", "sample_description": "Round-trip flight confirmation showing entry and exit.", "official_source_url": "https://evisa.go.ke/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Hotel Booking / Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in Kenya.", "sample_description": "Hotel or lodge booking confirmation. Safari lodge booking is acceptable.", "official_source_url": "https://evisa.go.ke/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of sufficient funds.", "sample_description": "3 months of bank statements showing sufficient funds.", "official_source_url": "https://evisa.go.ke/", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card. Kenya strictly requires proof of yellow fever vaccination.", "official_source_url": "https://evisa.go.ke/", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "South Africa", "code": "ZAF", "flag_emoji": "🇿🇦"},
        "visa_type": {
            "name": "South Africa Tourist Visa",
            "category": "tourist",
            "processing_time": "3–5 weeks",
            "fee_usd": "0.00",
            "validity": "Up to 90 days",
            "description": (
                "Nigerian nationals require a tourist visa to enter South Africa. "
                "Applications are submitted in person at the South African High Commission in Abuja "
                "or the Consulate General in Lagos. Biometrics are enrolled at the time of application. "
                "The visa itself has no application fee but service fees may apply. "
                "Strong financial documents and a clear itinerary are essential."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 30 days beyond intended return date. Must have at least 2 blank pages.", "official_source_url": "https://www.dha.gov.za/index.php/civic-services/apply-for-a-visa", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed BI-84 Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "South African visa application form.", "sample_description": "Download Form BI-84 from the DHA website. Complete in full, sign and submit in person.", "official_source_url": "https://www.dha.gov.za/index.php/civic-services/apply-for-a-visa", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Recent colour photographs.", "sample_description": "2 recent colour photos, 35mm x 45mm, white background.", "official_source_url": "https://www.dha.gov.za/index.php/civic-services/apply-for-a-visa", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "3–6 months of bank statements stamped by the bank. Must show sufficient funds for the trip.", "official_source_url": "https://www.dha.gov.za/index.php/civic-services/apply-for-a-visa", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Proof of Employment", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of stable employment in Nigeria.", "sample_description": "Employer letter on letterhead with role, salary, leave approval. Self-employed: CAC and business statements.", "official_source_url": "https://www.dha.gov.za/index.php/civic-services/apply-for-a-visa", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Return Flight Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight confirmation.", "sample_description": "Round-trip booking showing entry and exit.", "official_source_url": "https://www.dha.gov.za/index.php/civic-services/apply-for-a-visa", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Hotel Booking / Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in South Africa.", "sample_description": "Hotel booking for the full stay or invitation letter from a South African host with their ID and proof of address.", "official_source_url": "https://www.dha.gov.za/index.php/civic-services/apply-for-a-visa", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Travel Itinerary", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Planned South Africa activities.", "sample_description": "Day-by-day plan of cities to visit and activities. If combining with other Southern African countries, list all.", "official_source_url": "https://www.dha.gov.za/index.php/civic-services/apply-for-a-visa", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Medical coverage for South Africa.", "sample_description": "Policy covering the full trip, including medical emergencies.", "official_source_url": "https://www.dha.gov.za/index.php/civic-services/apply-for-a-visa", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.dha.gov.za/index.php/civic-services/apply-for-a-visa", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Ghana", "code": "GHA", "flag_emoji": "🇬🇭"},
        "visa_type": {
            "name": "Ghana Tourist Visa",
            "category": "tourist",
            "processing_time": "3–5 business days",
            "fee_usd": "60.00",
            "validity": "30 days (extendable)",
            "description": (
                "Nigerian nationals can apply for a Ghanaian tourist visa through the Ghana High Commission "
                "in Abuja or the Consulate in Lagos, or online through the Ghana Immigration Service e-Visa portal. "
                "Ghana is a popular short-trip destination for Nigerians. ECOWAS citizens technically do not "
                "need a visa, but Nigerian passport holders should confirm current requirements as policies vary."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 6 months beyond travel date.", "official_source_url": "https://immigration.gov.gh/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Ghana visa application form.", "sample_description": "Available online at the Ghana Immigration Service portal or at the High Commission. Complete and sign.", "official_source_url": "https://immigration.gov.gh/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Recent colour photographs.", "sample_description": "2 recent colour photos, white background.", "official_source_url": "https://immigration.gov.gh/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Return Flight Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Proof of onward travel.", "sample_description": "Round-trip flight booking showing entry and exit.", "official_source_url": "https://immigration.gov.gh/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Hotel Booking", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in Ghana.", "sample_description": "Hotel booking confirmation for the full stay.", "official_source_url": "https://immigration.gov.gh/", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "3 months of bank statements showing sufficient funds.", "official_source_url": "https://immigration.gov.gh/", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for all travellers to Ghana.", "sample_description": "Original yellow card. Ghana strictly requires this even for Nigerian nationals.", "official_source_url": "https://immigration.gov.gh/", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Ethiopia", "code": "ETH", "flag_emoji": "🇪🇹"},
        "visa_type": {
            "name": "Ethiopia e-Visa",
            "category": "tourist",
            "processing_time": "3–5 business days",
            "fee_usd": "72.00",
            "validity": "30 days single entry",
            "description": (
                "Nigerian nationals can apply for an Ethiopian e-Visa online at evisa.gov.et. "
                "Ethiopia is a growing tourist destination and a major African hub via Ethiopian Airlines. "
                "The e-Visa is straightforward and no embassy visit is required. "
                "Addis Ababa is also a popular stopover city."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 6 months beyond travel date. Scanned biodata page required.", "official_source_url": "https://www.evisa.gov.et/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Passport Photograph (Digital)", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Digital colour photo.", "sample_description": "Recent colour photo, white background, uploaded during the online application.", "official_source_url": "https://www.evisa.gov.et/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Return Flight Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Proof of onward travel.", "sample_description": "Round-trip flight confirmation.", "official_source_url": "https://www.evisa.gov.et/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Hotel Booking", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in Ethiopia.", "sample_description": "Hotel reservation for the full stay.", "official_source_url": "https://www.evisa.gov.et/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.evisa.gov.et/", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Brazil", "code": "BRA", "flag_emoji": "🇧🇷"},
        "visa_type": {
            "name": "Brazil Tourist Visa",
            "category": "tourist",
            "processing_time": "5–10 business days",
            "fee_usd": "80.00",
            "validity": "90 days per visit, multiple entry within 10 years",
            "description": (
                "Nigerian nationals must apply for a Brazilian tourist visa at the Brazilian Embassy in Abuja. "
                "Brazil requires a full in-person application with biometrics. "
                "Financial documentation and proof of ties to Nigeria are critical. "
                "Brazil is popular among Nigerian travellers for tourism and business during events like Carnival."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 6 months beyond intended stay. Must have at least 2 blank pages.", "official_source_url": "https://www.gov.br/mre/en/subjects/consular-services/visas/visa-information", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Brazilian consulate application form.", "sample_description": "Complete the online form at the Brazilian consulate portal. Print, sign and submit in person with all documents.", "official_source_url": "https://www.gov.br/mre/en/subjects/consular-services/visas/visa-information", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Recent colour photographs.", "sample_description": "2 recent colour photos, white background, 3cm x 4cm.", "official_source_url": "https://www.gov.br/mre/en/subjects/consular-services/visas/visa-information", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of bank statements stamped by the bank. Recommend BRL 500+ per day equivalent.", "official_source_url": "https://www.gov.br/mre/en/subjects/consular-services/visas/visa-information", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Proof of Employment", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of stable employment.", "sample_description": "Employer letter on letterhead with role, salary, leave. Self-employed: CAC and business statements.", "official_source_url": "https://www.gov.br/mre/en/subjects/consular-services/visas/visa-information", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Return Flight Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight confirmation.", "sample_description": "Round-trip booking showing entry and exit.", "official_source_url": "https://www.gov.br/mre/en/subjects/consular-services/visas/visa-information", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Hotel Booking", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in Brazil.", "sample_description": "Hotel booking for the full stay.", "official_source_url": "https://www.gov.br/mre/en/subjects/consular-services/visas/visa-information", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Proof of Ties to Nigeria", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Evidence you will return to Nigeria.", "sample_description": "Property deed, marriage certificate, dependants' birth certificates.", "official_source_url": "https://www.gov.br/mre/en/subjects/consular-services/visas/visa-information", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.gov.br/mre/en/subjects/consular-services/visas/visa-information", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "Mexico", "code": "MEX", "flag_emoji": "🇲🇽"},
        "visa_type": {
            "name": "Mexico Tourist Visa (FMM)",
            "category": "tourist",
            "processing_time": "1–2 weeks",
            "fee_usd": "36.00",
            "validity": "180 days (single entry)",
            "description": (
                "Nigerian nationals require a Mexican tourist visa (Forma Migratoria Múltiple – FMM). "
                "Applications are submitted at the Mexican Embassy in Abuja. "
                "Nigerians holding a valid US, Canadian, UK, EU, or Japanese visa may be eligible "
                "for a simplified entry process or may enter Mexico without a separate visa — "
                "check current exemptions before applying."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 6 months beyond intended stay.", "official_source_url": "https://embamex.sre.gob.mx/nigeria/index.php/en/", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Completed Visa Application Form", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "Mexican consulate application form.", "sample_description": "Download from the Mexican Embassy website. Complete, sign and submit in person.", "official_source_url": "https://embamex.sre.gob.mx/nigeria/index.php/en/", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Recent colour photographs.", "sample_description": "2 recent colour photos, white background, taken within 6 months.", "official_source_url": "https://embamex.sre.gob.mx/nigeria/index.php/en/", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "3–6 months of bank statements showing sufficient funds.", "official_source_url": "https://embamex.sre.gob.mx/nigeria/index.php/en/", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Proof of Employment", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of stable employment.", "sample_description": "Employer letter on letterhead. Self-employed: CAC and business statements.", "official_source_url": "https://embamex.sre.gob.mx/nigeria/index.php/en/", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Return Flight Booking", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Return flight confirmation.", "sample_description": "Round-trip booking confirmation.", "official_source_url": "https://embamex.sre.gob.mx/nigeria/index.php/en/", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Hotel Booking", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay in Mexico.", "sample_description": "Hotel booking for the full stay.", "official_source_url": "https://embamex.sre.gob.mx/nigeria/index.php/en/", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Valid US / Canada / UK / Schengen Visa", "icon_category": "travel", "importance": "conditional", "condition_note": "If applicable — may exempt from visa or simplify process.", "description": "Third-country visa that may enable simplified Mexico entry.", "sample_description": "Copy of a valid (not expired) US, UK, Canadian, or Schengen visa. Nigeria passport holders with valid visas to these countries may qualify for Mexico visa exemption.", "official_source_url": "https://embamex.sre.gob.mx/nigeria/index.php/en/", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://embamex.sre.gob.mx/nigeria/index.php/en/", "last_verified": "2026-06-01"},
        ],
    },

    {
        "country": {"name": "New Zealand", "code": "NZL", "flag_emoji": "🇳🇿"},
        "visa_type": {
            "name": "New Zealand Visitor Visa",
            "category": "tourist",
            "processing_time": "4–8 weeks",
            "fee_usd": "110.00",
            "validity": "Up to 9 months",
            "description": (
                "Nigerian nationals must apply for a New Zealand Visitor Visa online through the Immigration "
                "New Zealand portal. Applications are submitted digitally and no embassy visit is needed "
                "for the initial application. However, biometrics may be required at a designated centre. "
                "Financial documentation and genuine tourist intent must be clearly demonstrated."
            ),
        },
        "documents": [
            {"order": 1, "name": "International Passport", "icon_category": "passport", "importance": "mandatory", "condition_note": "", "description": "Valid travel document.", "sample_description": "Valid for at least 3 months beyond your departure from New Zealand. Include previous passports.", "official_source_url": "https://www.immigration.govt.nz/new-zealand-visas/apply-for-a-visa/about-visa/visitor-visa", "last_verified": "2026-06-01"},
            {"order": 2, "name": "Online Visa Application (INZ 1017)", "icon_category": "other", "importance": "mandatory", "condition_note": "", "description": "New Zealand online visa application.", "sample_description": "Apply online at Immigration New Zealand's RealMe portal. All documents are submitted digitally.", "official_source_url": "https://www.immigration.govt.nz/new-zealand-visas/apply-for-a-visa/about-visa/visitor-visa", "last_verified": "2026-06-01"},
            {"order": 3, "name": "Passport Photographs", "icon_category": "photo", "importance": "mandatory", "condition_note": "", "description": "Recent colour photographs.", "sample_description": "Recent colour photo uploaded digitally as part of the online application.", "official_source_url": "https://www.immigration.govt.nz/new-zealand-visas/apply-for-a-visa/about-visa/visitor-visa", "last_verified": "2026-06-01"},
            {"order": 4, "name": "Bank Statements", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Proof of financial means.", "sample_description": "6 months of bank statements. Recommend NZD 1,000+ per month of intended stay.", "official_source_url": "https://www.immigration.govt.nz/new-zealand-visas/apply-for-a-visa/about-visa/visitor-visa", "last_verified": "2026-06-01"},
            {"order": 5, "name": "Proof of Employment", "icon_category": "employment", "importance": "mandatory", "condition_note": "", "description": "Evidence of stable employment in Nigeria.", "sample_description": "Employer letter on letterhead with role, salary, leave. Self-employed: CAC and business statements.", "official_source_url": "https://www.immigration.govt.nz/new-zealand-visas/apply-for-a-visa/about-visa/visitor-visa", "last_verified": "2026-06-01"},
            {"order": 6, "name": "Payslips", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Income corroboration.", "sample_description": "Last 3–6 months of payslips.", "official_source_url": "https://www.immigration.govt.nz/new-zealand-visas/apply-for-a-visa/about-visa/visitor-visa", "last_verified": "2026-06-01"},
            {"order": 7, "name": "Travel Itinerary", "icon_category": "travel", "importance": "mandatory", "condition_note": "", "description": "Planned New Zealand activities.", "sample_description": "Flight booking and proposed itinerary covering key destinations.", "official_source_url": "https://www.immigration.govt.nz/new-zealand-visas/apply-for-a-visa/about-visa/visitor-visa", "last_verified": "2026-06-01"},
            {"order": 8, "name": "Accommodation Proof", "icon_category": "accommodation", "importance": "mandatory", "condition_note": "", "description": "Where you will stay.", "sample_description": "Hotel bookings for the trip or host invitation letter with NZ residency proof.", "official_source_url": "https://www.immigration.govt.nz/new-zealand-visas/apply-for-a-visa/about-visa/visitor-visa", "last_verified": "2026-06-01"},
            {"order": 9, "name": "Proof of Ties to Nigeria", "icon_category": "financial", "importance": "mandatory", "condition_note": "", "description": "Evidence you will return to Nigeria.", "sample_description": "Property deed, marriage certificate, birth certificates of dependants.", "official_source_url": "https://www.immigration.govt.nz/new-zealand-visas/apply-for-a-visa/about-visa/visitor-visa", "last_verified": "2026-06-01"},
            {"order": 10, "name": "Travel Insurance", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Medical coverage for New Zealand.", "sample_description": "Policy covering the full trip, including medical treatment and repatriation.", "official_source_url": "https://www.immigration.govt.nz/new-zealand-visas/apply-for-a-visa/about-visa/visitor-visa", "last_verified": "2026-06-01"},
            {"order": 11, "name": "Yellow Fever Vaccination Card", "icon_category": "medical", "importance": "mandatory", "condition_note": "", "description": "Required for Nigerian travellers.", "sample_description": "Original yellow card.", "official_source_url": "https://www.immigration.govt.nz/new-zealand-visas/apply-for-a-visa/about-visa/visitor-visa", "last_verified": "2026-06-01"},
        ],
    },
]


class Command(BaseCommand):
    help = "Populates the database with visa data for all groups (Big Five, Schengen, Asia-Pacific, Middle East/Africa/Americas)"

    def handle(self, *args, **kwargs):
        country_codes = [entry["country"]["code"] for entry in DATA]
        deleted_count, _ = Country.objects.filter(code__in=country_codes).delete()
        self.stdout.write(self.style.WARNING(
            f"Deleted data for {len(country_codes)} countries ({deleted_count} total objects deleted)."
        ))

        created_countries = 0
        created_visas = 0
        created_docs = 0

        for entry in DATA:
            # --- Country ---
            country, c_created = Country.objects.update_or_create(
                code=entry["country"]["code"],
                defaults={
                    "name": entry["country"]["name"],
                    "flag_emoji": entry["country"]["flag_emoji"],
                },
            )
            if c_created:
                created_countries += 1
                self.stdout.write(f"  Created country: {country.name}")
            else:
                self.stdout.write(f"  Country already exists: {country.name}")

            # --- VisaType ---
            vt_data = entry["visa_type"]
            fee_usd = Decimal(vt_data["fee_usd"]) if vt_data.get("fee_usd") else None
            visa_type, vt_created = VisaType.objects.update_or_create(
                country=country,
                name=vt_data["name"],
                defaults={
                    "category": vt_data["category"],
                    "processing_time": vt_data["processing_time"],
                    "fee_usd": fee_usd,
                    "validity": vt_data["validity"],
                    "description": vt_data["description"],
                    "is_active": True,
                },
            )
            if vt_created:
                created_visas += 1
                self.stdout.write(f"    Created visa type: {visa_type.name}")
            else:
                self.stdout.write(f"    Visa type already exists: {visa_type.name}")

            # --- DocumentRequirements ---
            for doc in entry["documents"]:
                _, doc_created = DocumentRequirement.objects.update_or_create(
                    visa_type=visa_type,
                    name=doc["name"],
                    defaults={
                        "description": doc.get("description", ""),
                        "icon_category": doc.get("icon_category", "other"),
                        "importance": doc.get("importance", "mandatory"),
                        "condition_note": doc.get("condition_note", ""),
                        "sample_description": doc.get("sample_description", ""),
                        "official_source_url": doc.get("official_source_url", ""),
                        "last_verified": parse_date(doc.get("last_verified")) if doc.get("last_verified") else None,
                        "order": doc.get("order", 0),
                    },
                )
                if doc_created:
                    created_docs += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Created: {created_countries} countries, "
            f"{created_visas} visa types, {created_docs} document requirements."
        ))
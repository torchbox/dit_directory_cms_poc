import json

from find_a_supplier import models as find_a_supplier
from export_readiness import models as export_readiness
from invest import models as invest
from components import models as components
from great_international import models as great_international

# Extract field definitions for all page models listed here.
# Output: cms-fields.json
# Execution:
# make debug_manage cmd=shell
# from core.help_review import save_all_fields_json; save_all_fields_json()

# Hard-coded list of page models to inspect.
page_models = {
    "find_a_supplier.IndustryPage": find_a_supplier.IndustryPage,
    "find_a_supplier.LandingPage": find_a_supplier.LandingPage,
    "find_a_supplier.IndustryLandingPage": find_a_supplier.IndustryLandingPage,
    "find_a_supplier.IndustryArticlePage": find_a_supplier.IndustryArticlePage,
    "export_readiness.ExportReadinessApp": export_readiness.ExportReadinessApp,
    "find_a_supplier.FindASupplierApp": find_a_supplier.FindASupplierApp,
    "export_readiness.PrivacyAndCookiesPage": export_readiness.PrivacyAndCookiesPage,
    "find_a_supplier.IndustryContactPage": find_a_supplier.IndustryContactPage,
    "export_readiness.TermsAndConditionsPage": export_readiness.TermsAndConditionsPage,
    "export_readiness.PerformanceDashboardPage": export_readiness.PerformanceDashboardPage,
    "export_readiness.PerformanceDashboardNotesPage": export_readiness.PerformanceDashboardNotesPage,
    "invest.InvestApp": invest.InvestApp,
    "invest.InvestHomePage": invest.InvestHomePage,
    "invest.SetupGuideLandingPage": invest.SetupGuideLandingPage,
    "invest.SectorLandingPage": invest.SectorLandingPage,
    "invest.SectorPage": invest.SectorPage,
    "invest.RegionLandingPage": invest.RegionLandingPage,
    "invest.SetupGuidePage": invest.SetupGuidePage,
    "export_readiness.GetFinancePage": export_readiness.GetFinancePage,
    "invest.HighPotentialOpportunityDetailPage": invest.HighPotentialOpportunityDetailPage,
    "invest.HighPotentialOpportunityFormPage": invest.HighPotentialOpportunityFormPage,
    "invest.HighPotentialOpportunityFormSuccessPage": invest.HighPotentialOpportunityFormSuccessPage,
    "export_readiness.EUExitInternationalFormPage": export_readiness.EUExitInternationalFormPage,
    "export_readiness.EUExitDomesticFormPage": export_readiness.EUExitDomesticFormPage,
    "export_readiness.EUExitFormSuccessPage": export_readiness.EUExitFormSuccessPage,
    "export_readiness.TopicLandingPage": export_readiness.TopicLandingPage,
    "export_readiness.HomePage": export_readiness.HomePage,
    "export_readiness.InternationalLandingPage": export_readiness.InternationalLandingPage,
    "export_readiness.ArticleListingPage": export_readiness.ArticleListingPage,
    "components.ComponentsApp": components.ComponentsApp,
    "components.BannerComponent": components.BannerComponent,
    "export_readiness.ArticlePage": export_readiness.ArticlePage,
    "export_readiness.ContactUsGuidancePage": export_readiness.ContactUsGuidancePage,
    "export_readiness.ContactSuccessPage": export_readiness.ContactSuccessPage,
    "export_readiness.ContactSuccessPages": export_readiness.ContactSuccessPages,
    "export_readiness.ContactUsGuidancePages": export_readiness.ContactUsGuidancePages,
    "export_readiness.CampaignPage": export_readiness.CampaignPage,
    "export_readiness.SitePolicyPages": export_readiness.SitePolicyPages,
    "export_readiness.MarketingPages": export_readiness.MarketingPages,
    "great_international.GreatInternationalApp": great_international.GreatInternationalApp,
    "great_international.InternationalHomePage": great_international.InternationalHomePage,
    "great_international.InternationalCampaignPage": great_international.InternationalCampaignPage,
    "great_international.InternationalArticlePage": great_international.InternationalArticlePage,
    "great_international.InternationalRegionPage": great_international.InternationalRegionPage,
    "great_international.InternationalLocalisedFolderPage": great_international.InternationalLocalisedFolderPage,
    "great_international.InternationalTopicLandingPage": great_international.InternationalTopicLandingPage,
    "great_international.InternationalSectorPage": great_international.InternationalSectorPage,
    "export_readiness.CountryGuidePage": export_readiness.CountryGuidePage,
    "great_international.InternationalArticleListingPage": great_international.InternationalArticleListingPage,
    "great_international.InternationalCuratedTopicLandingPage": great_international.InternationalCuratedTopicLandingPage,
    "great_international.InternationalGuideLandingPage": great_international.InternationalGuideLandingPage,
}

excluded_field_patterns = [
    # Not relevant.
    "wagtailforms",
    # Core fields that are not user-editable, or relevant to the review.
    "wagtailcore.site",
    "wagtailcore.pagerevision",
    "wagtailcore.grouppagepermission",
    "wagtailcore.pageviewrestriction",
    "wagtailcore.Page.id",
    "wagtailcore.Page.path",
    "wagtailcore.Page.depth",
    "wagtailcore.Page.numchild",
    "wagtailcore.Page.draft_title",
    "wagtailcore.Page.content_type",
    "wagtailcore.Page.live",
    "wagtailcore.Page.has_unpublished_changes",
    "wagtailcore.Page.url_path",
    "wagtailcore.Page.owner",
    "wagtailcore.Page.expired",
    "wagtailcore.Page.locked",
    "wagtailcore.Page.live_revision",
    "wagtailcore.Page.show_in_menus",
    "wagtailcore.Page.go_live_at",
    "wagtailcore.Page.expire_at",
    "wagtailcore.Page.first_published_at",
    "wagtailcore.Page.last_published_at",
    "wagtailcore.Page.latest_revision_created_at",
    # Translations internal field.
    ".page_ptr",
    # Page relations
    "ManyToOneRel",
    "OneToOneRel",
    # User fields shared between all pages.
    "wagtailcore.Page.title",
    "wagtailcore.Page.slug",
    "wagtailcore.Page.seo_title",
    "wagtailcore.Page.search_description",
    # Custom fields invisible to the end user.
    ".service_name",
]


def get_all_fields():
    page_types = {}

    for model_name in page_models:
        model = page_models[model_name]
        raw_fields = model._meta.get_fields()
        fields = []

        for raw_field in raw_fields:
            name = str(raw_field)
            type_ = str(type(raw_field)).replace("<class '", "").replace("'>", "")

            # Do not export fields that match an exclude pattern, or that are translation fields.
            is_excluded = (
                any(pattern in name for pattern in excluded_field_patterns)
                or "TranslationFieldSpecific" in type_
            )

            if not is_excluded:
                verbose_name = (
                    str(raw_field.verbose_name)
                    if hasattr(raw_field, "verbose_name")
                    else ""
                )

                field = {
                    "name": name,
                    "verbose_name": verbose_name.capitalize(),
                    "type": type_,
                    "help_text": str(raw_field.help_text)
                    if hasattr(raw_field, "help_text")
                    else "",
                }
                fields.append(field)

        page_types[model_name] = fields

    return page_types


def save_all_fields_json():
    with open("cms-fields.json", "w") as j:
        j.write(json.dumps(get_all_fields(), indent=2))

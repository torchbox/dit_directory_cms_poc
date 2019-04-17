import json

from find_a_supplier import models as find_a_supplier
from export_readiness import models as export_readiness
from invest import models as invest
from components import models as components
from great_international import models as great_international

# make debug_manage cmd=shell
# from core.markdown_review import get_all_markdown_json; get_all_markdown_json()

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


markdown_fields = {
    "find_a_supplier.IndustryPage": [
        "hero_text",
        "introduction_column_one_text",
        "introduction_column_two_text",
        "introduction_column_three_text",
        "company_list_text",
    ],
    "find_a_supplier.LandingPage": [
        "hero_text",
        "proposition_text",
        "industries_list_text",
        "services_list_text",
        "services_column_one",
        "services_column_two",
        "services_column_three",
        "services_column_four",
    ],
    "find_a_supplier.IndustryArticlePage": ["body"],
    "export_readiness.PrivacyAndCookiesPage": ["body"],
    "find_a_supplier.IndustryContactPage": [
        "introduction_text",
        "success_message_text",
    ],
    "export_readiness.TermsAndConditionsPage": ["body"],
    "export_readiness.PerformanceDashboardPage": [
        "description",
        "data_description_row_one",
        "data_description_row_two",
        "data_description_row_three",
        "data_description_row_four",
        "guidance_notes",
    ],
    "export_readiness.PerformanceDashboardNotesPage": ["body"],
    "invest.InvestHomePage": [
        "benefits_section_content",
        "eu_exit_section_content",
        "subsection_content_one",
        "subsection_content_two",
        "subsection_content_three",
        "subsection_content_four",
        "subsection_content_five",
        "subsection_content_six",
        "subsection_content_seven",
        "setup_guide_content",
    ],
    "invest.SectorPage": [
        "pullout_text",
        "subsection_content_one",
        "subsection_content_two",
        "subsection_content_three",
        "subsection_content_four",
        "subsection_content_five",
        "subsection_content_six",
        "subsection_content_seven",
    ],
    "invest.SetupGuidePage": [
        "subsection_content_one",
        "subsection_content_two",
        "subsection_content_three",
        "subsection_content_four",
        "subsection_content_five",
        "subsection_content_six",
        "subsection_content_seven",
    ],
    "export_readiness.GetFinancePage": [
        "hero_text",
        "contact_proposition",
        "advantages_one",
        "advantages_two",
        "advantages_three",
        "evidence",
    ],
    "invest.HighPotentialOpportunityDetailPage": [
        "contact_proposition",
        "proposition_one",
        "opportunity_list_item_one",
        "opportunity_list_item_two",
        "opportunity_list_item_three",
        "proposition_two",
        "proposition_two_list_item_one",
        "proposition_two_list_item_two",
        "proposition_two_list_item_three",
        "competitive_advantages_list_item_one",
        "competitive_advantages_list_item_two",
        "competitive_advantages_list_item_three",
        "testimonial",
        "companies_list_text",
        "case_study_one_text",
        "case_study_two_text",
        "case_study_three_text",
        "case_study_four_text",
    ],
    "export_readiness.EUExitInternationalFormPage": ["body_text"],
    "export_readiness.EUExitDomesticFormPage": ["body_text"],
    "export_readiness.HomePage": ["banner_content", "news_description"],
    "export_readiness.ArticleListingPage": ["list_teaser"],
    "components.BannerComponent": ["banner_content"],
    "export_readiness.ArticlePage": ["article_body_text"],
    "export_readiness.ContactUsGuidancePage": ["body"],
    "export_readiness.CampaignPage": [
        "section_one_intro",
        "selling_point_one_content",
        "selling_point_two_content",
        "selling_point_three_content",
        "section_two_intro",
        "related_content_intro",
    ],
    "great_international.InternationalHomePage": [
        # "invest_content",
        "trade_content",
        "tariffs_description",
    ],
    "great_international.InternationalCampaignPage": [
        "section_one_intro",
        "selling_point_one_content",
        "selling_point_two_content",
        "selling_point_three_content",
        "section_two_intro",
        "related_content_intro",
    ],
    "great_international.InternationalArticlePage": ["article_body_text"],
    "great_international.InternationalSectorPage": [
        "section_one_body",
        "section_three_subsection_one_body",
        "section_three_subsection_two_body",
    ],
    "export_readiness.CountryGuidePage": [
        "section_one_body",
        "fact_sheet_column_1_body",
        "fact_sheet_column_2_body",
    ],
    "great_international.InternationalArticleListingPage": ["list_teaser"],
    "great_international.InternationalCuratedTopicLandingPage": [
        "feature_one_content",
        "feature_two_content",
    ],
    "great_international.InternationalGuideLandingPage": ["section_one_content"],
}


def get_all_markdown():
    values = []

    for model_name in page_models:
        model = page_models[model_name]
        fields = markdown_fields[model_name]

        for field in fields:
            for value in model.objects.values_list(field):
                values.append(value)

    return values


def get_all_markdown_json():
    with open("markdown.json", "w") as j:
        j.write(json.dumps(get_all_markdown(), indent=2))

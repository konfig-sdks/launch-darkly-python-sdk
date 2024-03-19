import typing_extensions

from launch_darkly_python_sdk.apis.tags import TagValues
from launch_darkly_python_sdk.apis.tags.segments_api import SegmentsApi
from launch_darkly_python_sdk.apis.tags.approvals_api import ApprovalsApi
from launch_darkly_python_sdk.apis.tags.code_references_api import CodeReferencesApi
from launch_darkly_python_sdk.apis.tags.feature_flags_api import FeatureFlagsApi
from launch_darkly_python_sdk.apis.tags.account_usage_beta_api import AccountUsageBetaApi
from launch_darkly_python_sdk.apis.tags.contexts_api import ContextsApi
from launch_darkly_python_sdk.apis.tags.experiments_beta_api import ExperimentsBetaApi
from launch_darkly_python_sdk.apis.tags.projects_api import ProjectsApi
from launch_darkly_python_sdk.apis.tags.teams_api import TeamsApi
from launch_darkly_python_sdk.apis.tags.applications_beta_api import ApplicationsBetaApi
from launch_darkly_python_sdk.apis.tags.environments_api import EnvironmentsApi
from launch_darkly_python_sdk.apis.tags.integration_delivery_configurations_beta_api import IntegrationDeliveryConfigurationsBetaApi
from launch_darkly_python_sdk.apis.tags.access_tokens_api import AccessTokensApi
from launch_darkly_python_sdk.apis.tags.account_members_api import AccountMembersApi
from launch_darkly_python_sdk.apis.tags.insights_scores_beta_api import InsightsScoresBetaApi
from launch_darkly_python_sdk.apis.tags.relay_proxy_configurations_api import RelayProxyConfigurationsApi
from launch_darkly_python_sdk.apis.tags.custom_roles_api import CustomRolesApi
from launch_darkly_python_sdk.apis.tags.data_export_destinations_api import DataExportDestinationsApi
from launch_darkly_python_sdk.apis.tags.flag_triggers_api import FlagTriggersApi
from launch_darkly_python_sdk.apis.tags.insights_charts_beta_api import InsightsChartsBetaApi
from launch_darkly_python_sdk.apis.tags.integration_audit_log_subscriptions_api import IntegrationAuditLogSubscriptionsApi
from launch_darkly_python_sdk.apis.tags.integrations_beta_api import IntegrationsBetaApi
from launch_darkly_python_sdk.apis.tags.metrics_api import MetricsApi
from launch_darkly_python_sdk.apis.tags.metrics_beta_api import MetricsBetaApi
from launch_darkly_python_sdk.apis.tags.o_auth2_clients_api import OAuth2ClientsApi
from launch_darkly_python_sdk.apis.tags.release_pipelines_beta_api import ReleasePipelinesBetaApi
from launch_darkly_python_sdk.apis.tags.scheduled_changes_api import ScheduledChangesApi
from launch_darkly_python_sdk.apis.tags.user_settings_api import UserSettingsApi
from launch_darkly_python_sdk.apis.tags.webhooks_api import WebhooksApi
from launch_darkly_python_sdk.apis.tags.flag_links_beta_api import FlagLinksBetaApi
from launch_darkly_python_sdk.apis.tags.follow_flags_api import FollowFlagsApi
from launch_darkly_python_sdk.apis.tags.insights_deployments_beta_api import InsightsDeploymentsBetaApi
from launch_darkly_python_sdk.apis.tags.segments_beta_api import SegmentsBetaApi
from launch_darkly_python_sdk.apis.tags.users_api import UsersApi
from launch_darkly_python_sdk.apis.tags.workflows_api import WorkflowsApi
from launch_darkly_python_sdk.apis.tags.other_api import OtherApi
from launch_darkly_python_sdk.apis.tags.feature_flags_beta_api import FeatureFlagsBetaApi
from launch_darkly_python_sdk.apis.tags.insights_repositories_beta_api import InsightsRepositoriesBetaApi
from launch_darkly_python_sdk.apis.tags.workflow_templates_api import WorkflowTemplatesApi
from launch_darkly_python_sdk.apis.tags.audit_log_api import AuditLogApi
from launch_darkly_python_sdk.apis.tags.releases_beta_api import ReleasesBetaApi
from launch_darkly_python_sdk.apis.tags.account_members_beta_api import AccountMembersBetaApi
from launch_darkly_python_sdk.apis.tags.context_settings_api import ContextSettingsApi
from launch_darkly_python_sdk.apis.tags.insights_flag_events_beta_api import InsightsFlagEventsBetaApi
from launch_darkly_python_sdk.apis.tags.insights_pull_requests_beta_api import InsightsPullRequestsBetaApi
from launch_darkly_python_sdk.apis.tags.tags_api import TagsApi
from launch_darkly_python_sdk.apis.tags.teams_beta_api import TeamsBetaApi
from launch_darkly_python_sdk.apis.tags.users_beta_api import UsersBetaApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.SEGMENTS: SegmentsApi,
        TagValues.APPROVALS: ApprovalsApi,
        TagValues.CODE_REFERENCES: CodeReferencesApi,
        TagValues.FEATURE_FLAGS: FeatureFlagsApi,
        TagValues.ACCOUNT_USAGE_BETA: AccountUsageBetaApi,
        TagValues.CONTEXTS: ContextsApi,
        TagValues.EXPERIMENTS_BETA: ExperimentsBetaApi,
        TagValues.PROJECTS: ProjectsApi,
        TagValues.TEAMS: TeamsApi,
        TagValues.APPLICATIONS_BETA: ApplicationsBetaApi,
        TagValues.ENVIRONMENTS: EnvironmentsApi,
        TagValues.INTEGRATION_DELIVERY_CONFIGURATIONS_BETA: IntegrationDeliveryConfigurationsBetaApi,
        TagValues.ACCESS_TOKENS: AccessTokensApi,
        TagValues.ACCOUNT_MEMBERS: AccountMembersApi,
        TagValues.INSIGHTS_SCORES_BETA: InsightsScoresBetaApi,
        TagValues.RELAY_PROXY_CONFIGURATIONS: RelayProxyConfigurationsApi,
        TagValues.CUSTOM_ROLES: CustomRolesApi,
        TagValues.DATA_EXPORT_DESTINATIONS: DataExportDestinationsApi,
        TagValues.FLAG_TRIGGERS: FlagTriggersApi,
        TagValues.INSIGHTS_CHARTS_BETA: InsightsChartsBetaApi,
        TagValues.INTEGRATION_AUDIT_LOG_SUBSCRIPTIONS: IntegrationAuditLogSubscriptionsApi,
        TagValues.INTEGRATIONS_BETA: IntegrationsBetaApi,
        TagValues.METRICS: MetricsApi,
        TagValues.METRICS_BETA: MetricsBetaApi,
        TagValues.OAUTH2_CLIENTS: OAuth2ClientsApi,
        TagValues.RELEASE_PIPELINES_BETA: ReleasePipelinesBetaApi,
        TagValues.SCHEDULED_CHANGES: ScheduledChangesApi,
        TagValues.USER_SETTINGS: UserSettingsApi,
        TagValues.WEBHOOKS: WebhooksApi,
        TagValues.FLAG_LINKS_BETA: FlagLinksBetaApi,
        TagValues.FOLLOW_FLAGS: FollowFlagsApi,
        TagValues.INSIGHTS_DEPLOYMENTS_BETA: InsightsDeploymentsBetaApi,
        TagValues.SEGMENTS_BETA: SegmentsBetaApi,
        TagValues.USERS: UsersApi,
        TagValues.WORKFLOWS: WorkflowsApi,
        TagValues.OTHER: OtherApi,
        TagValues.FEATURE_FLAGS_BETA: FeatureFlagsBetaApi,
        TagValues.INSIGHTS_REPOSITORIES_BETA: InsightsRepositoriesBetaApi,
        TagValues.WORKFLOW_TEMPLATES: WorkflowTemplatesApi,
        TagValues.AUDIT_LOG: AuditLogApi,
        TagValues.RELEASES_BETA: ReleasesBetaApi,
        TagValues.ACCOUNT_MEMBERS_BETA: AccountMembersBetaApi,
        TagValues.CONTEXT_SETTINGS: ContextSettingsApi,
        TagValues.INSIGHTS_FLAG_EVENTS_BETA: InsightsFlagEventsBetaApi,
        TagValues.INSIGHTS_PULL_REQUESTS_BETA: InsightsPullRequestsBetaApi,
        TagValues.TAGS: TagsApi,
        TagValues.TEAMS_BETA: TeamsBetaApi,
        TagValues.USERS_BETA: UsersBetaApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.SEGMENTS: SegmentsApi,
        TagValues.APPROVALS: ApprovalsApi,
        TagValues.CODE_REFERENCES: CodeReferencesApi,
        TagValues.FEATURE_FLAGS: FeatureFlagsApi,
        TagValues.ACCOUNT_USAGE_BETA: AccountUsageBetaApi,
        TagValues.CONTEXTS: ContextsApi,
        TagValues.EXPERIMENTS_BETA: ExperimentsBetaApi,
        TagValues.PROJECTS: ProjectsApi,
        TagValues.TEAMS: TeamsApi,
        TagValues.APPLICATIONS_BETA: ApplicationsBetaApi,
        TagValues.ENVIRONMENTS: EnvironmentsApi,
        TagValues.INTEGRATION_DELIVERY_CONFIGURATIONS_BETA: IntegrationDeliveryConfigurationsBetaApi,
        TagValues.ACCESS_TOKENS: AccessTokensApi,
        TagValues.ACCOUNT_MEMBERS: AccountMembersApi,
        TagValues.INSIGHTS_SCORES_BETA: InsightsScoresBetaApi,
        TagValues.RELAY_PROXY_CONFIGURATIONS: RelayProxyConfigurationsApi,
        TagValues.CUSTOM_ROLES: CustomRolesApi,
        TagValues.DATA_EXPORT_DESTINATIONS: DataExportDestinationsApi,
        TagValues.FLAG_TRIGGERS: FlagTriggersApi,
        TagValues.INSIGHTS_CHARTS_BETA: InsightsChartsBetaApi,
        TagValues.INTEGRATION_AUDIT_LOG_SUBSCRIPTIONS: IntegrationAuditLogSubscriptionsApi,
        TagValues.INTEGRATIONS_BETA: IntegrationsBetaApi,
        TagValues.METRICS: MetricsApi,
        TagValues.METRICS_BETA: MetricsBetaApi,
        TagValues.OAUTH2_CLIENTS: OAuth2ClientsApi,
        TagValues.RELEASE_PIPELINES_BETA: ReleasePipelinesBetaApi,
        TagValues.SCHEDULED_CHANGES: ScheduledChangesApi,
        TagValues.USER_SETTINGS: UserSettingsApi,
        TagValues.WEBHOOKS: WebhooksApi,
        TagValues.FLAG_LINKS_BETA: FlagLinksBetaApi,
        TagValues.FOLLOW_FLAGS: FollowFlagsApi,
        TagValues.INSIGHTS_DEPLOYMENTS_BETA: InsightsDeploymentsBetaApi,
        TagValues.SEGMENTS_BETA: SegmentsBetaApi,
        TagValues.USERS: UsersApi,
        TagValues.WORKFLOWS: WorkflowsApi,
        TagValues.OTHER: OtherApi,
        TagValues.FEATURE_FLAGS_BETA: FeatureFlagsBetaApi,
        TagValues.INSIGHTS_REPOSITORIES_BETA: InsightsRepositoriesBetaApi,
        TagValues.WORKFLOW_TEMPLATES: WorkflowTemplatesApi,
        TagValues.AUDIT_LOG: AuditLogApi,
        TagValues.RELEASES_BETA: ReleasesBetaApi,
        TagValues.ACCOUNT_MEMBERS_BETA: AccountMembersBetaApi,
        TagValues.CONTEXT_SETTINGS: ContextSettingsApi,
        TagValues.INSIGHTS_FLAG_EVENTS_BETA: InsightsFlagEventsBetaApi,
        TagValues.INSIGHTS_PULL_REQUESTS_BETA: InsightsPullRequestsBetaApi,
        TagValues.TAGS: TagsApi,
        TagValues.TEAMS_BETA: TeamsBetaApi,
        TagValues.USERS_BETA: UsersBetaApi,
    }
)

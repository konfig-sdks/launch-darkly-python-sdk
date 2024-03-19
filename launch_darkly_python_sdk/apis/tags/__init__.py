# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from launch_darkly_python_sdk.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    SEGMENTS = "Segments"
    APPROVALS = "Approvals"
    CODE_REFERENCES = "Code references"
    FEATURE_FLAGS = "Feature flags"
    ACCOUNT_USAGE_BETA = "Account usage (beta)"
    CONTEXTS = "Contexts"
    EXPERIMENTS_BETA = "Experiments (beta)"
    PROJECTS = "Projects"
    TEAMS = "Teams"
    APPLICATIONS_BETA = "Applications (beta)"
    ENVIRONMENTS = "Environments"
    INTEGRATION_DELIVERY_CONFIGURATIONS_BETA = "Integration delivery configurations (beta)"
    ACCESS_TOKENS = "Access tokens"
    ACCOUNT_MEMBERS = "Account members"
    INSIGHTS_SCORES_BETA = "Insights scores (beta)"
    RELAY_PROXY_CONFIGURATIONS = "Relay Proxy configurations"
    CUSTOM_ROLES = "Custom roles"
    DATA_EXPORT_DESTINATIONS = "Data Export destinations"
    FLAG_TRIGGERS = "Flag triggers"
    INSIGHTS_CHARTS_BETA = "Insights charts (beta)"
    INTEGRATION_AUDIT_LOG_SUBSCRIPTIONS = "Integration audit log subscriptions"
    INTEGRATIONS_BETA = "Integrations (beta)"
    METRICS = "Metrics"
    METRICS_BETA = "Metrics (beta)"
    OAUTH2_CLIENTS = "OAuth2 Clients"
    RELEASE_PIPELINES_BETA = "Release pipelines (beta)"
    SCHEDULED_CHANGES = "Scheduled changes"
    USER_SETTINGS = "User settings"
    WEBHOOKS = "Webhooks"
    FLAG_LINKS_BETA = "Flag links (beta)"
    FOLLOW_FLAGS = "Follow flags"
    INSIGHTS_DEPLOYMENTS_BETA = "Insights deployments (beta)"
    SEGMENTS_BETA = "Segments (beta)"
    USERS = "Users"
    WORKFLOWS = "Workflows"
    OTHER = "Other"
    FEATURE_FLAGS_BETA = "Feature flags (beta)"
    INSIGHTS_REPOSITORIES_BETA = "Insights repositories (beta)"
    WORKFLOW_TEMPLATES = "Workflow templates"
    AUDIT_LOG = "Audit log"
    RELEASES_BETA = "Releases (beta)"
    ACCOUNT_MEMBERS_BETA = "Account members (beta)"
    CONTEXT_SETTINGS = "Context settings"
    INSIGHTS_FLAG_EVENTS_BETA = "Insights flag events (beta)"
    INSIGHTS_PULL_REQUESTS_BETA = "Insights pull requests (beta)"
    TAGS = "Tags"
    TEAMS_BETA = "Teams (beta)"
    USERS_BETA = "Users (beta)"

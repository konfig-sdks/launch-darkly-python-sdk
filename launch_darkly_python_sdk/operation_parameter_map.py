operation_parameter_map = {
    '/api/v2/tokens-POST': {
        'parameters': [
            {
                'name': 'description'
            },
            {
                'name': 'name'
            },
            {
                'name': 'role'
            },
            {
                'name': 'customRoleIds'
            },
            {
                'name': 'inlineRole'
            },
            {
                'name': 'serviceToken'
            },
            {
                'name': 'defaultApiVersion'
            },
        ]
    },
    '/api/v2/tokens/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/tokens/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/tokens-GET': {
        'parameters': [
            {
                'name': 'showAll'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
        ]
    },
    '/api/v2/tokens/{id}/reset-POST': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'expiry'
            },
        ]
    },
    '/api/v2/tokens/{id}-PATCH': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/members/{id}/teams-POST': {
        'parameters': [
            {
                'name': 'teamKeys'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/members/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/members/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/members-POST': {
        'parameters': [
        ]
    },
    '/api/v2/members-GET': {
        'parameters': [
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/api/v2/members/{id}-PATCH': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/members-PATCH': {
        'parameters': [
            {
                'name': 'instructions'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/usage/evaluations/{projectKey}/{environmentKey}/{featureFlagKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
            {
                'name': 'tz'
            },
        ]
    },
    '/api/v2/usage/events/{type}-GET': {
        'parameters': [
            {
                'name': 'type'
            },
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
        ]
    },
    '/api/v2/usage/experimentation-keys-GET': {
        'parameters': [
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
        ]
    },
    '/api/v2/usage/experimentation-units-GET': {
        'parameters': [
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
        ]
    },
    '/api/v2/usage/mau/bycategory-GET': {
        'parameters': [
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
        ]
    },
    '/api/v2/usage/mau-GET': {
        'parameters': [
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
            {
                'name': 'project'
            },
            {
                'name': 'environment'
            },
            {
                'name': 'sdktype'
            },
            {
                'name': 'sdk'
            },
            {
                'name': 'anonymous'
            },
            {
                'name': 'groupby'
            },
        ]
    },
    '/api/v2/usage/streams/{source}-GET': {
        'parameters': [
            {
                'name': 'source'
            },
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
            {
                'name': 'tz'
            },
        ]
    },
    '/api/v2/usage/streams/{source}/bysdkversion-GET': {
        'parameters': [
            {
                'name': 'source'
            },
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
            {
                'name': 'tz'
            },
            {
                'name': 'sdk'
            },
            {
                'name': 'version'
            },
        ]
    },
    '/api/v2/usage/mau/sdks-GET': {
        'parameters': [
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
            {
                'name': 'sdktype'
            },
        ]
    },
    '/api/v2/usage/streams/{source}/sdkversions-GET': {
        'parameters': [
            {
                'name': 'source'
            },
        ]
    },
    '/api/v2/applications/{applicationKey}-GET': {
        'parameters': [
            {
                'name': 'applicationKey'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/applications/{applicationKey}/versions-GET': {
        'parameters': [
            {
                'name': 'applicationKey'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/api/v2/applications-GET': {
        'parameters': [
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/applications/{applicationKey}-DELETE': {
        'parameters': [
            {
                'name': 'applicationKey'
            },
        ]
    },
    '/api/v2/applications/{applicationKey}/versions/{versionKey}-DELETE': {
        'parameters': [
            {
                'name': 'applicationKey'
            },
            {
                'name': 'versionKey'
            },
        ]
    },
    '/api/v2/applications/{applicationKey}-PATCH': {
        'parameters': [
            {
                'name': 'applicationKey'
            },
        ]
    },
    '/api/v2/applications/{applicationKey}/versions/{versionKey}-PATCH': {
        'parameters': [
            {
                'name': 'applicationKey'
            },
            {
                'name': 'versionKey'
            },
        ]
    },
    '/api/v2/approval-requests/{id}/apply-POST': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}/apply-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'id'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests-flag-copy-POST': {
        'parameters': [
            {
                'name': 'description'
            },
            {
                'name': 'source'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'comment'
            },
            {
                'name': 'notifyMemberIds'
            },
            {
                'name': 'notifyTeamKeys'
            },
            {
                'name': 'includedActions'
            },
            {
                'name': 'excludedActions'
            },
        ]
    },
    '/api/v2/approval-requests-POST': {
        'parameters': [
            {
                'name': 'description'
            },
            {
                'name': 'resourceId'
            },
            {
                'name': 'instructions'
            },
            {
                'name': 'comment'
            },
            {
                'name': 'notifyMemberIds'
            },
            {
                'name': 'notifyTeamKeys'
            },
            {
                'name': 'integrationConfig'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests-POST': {
        'parameters': [
            {
                'name': 'description'
            },
            {
                'name': 'instructions'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'comment'
            },
            {
                'name': 'notifyMemberIds'
            },
            {
                'name': 'notifyTeamKeys'
            },
            {
                'name': 'executionDate'
            },
            {
                'name': 'operatingOnId'
            },
            {
                'name': 'integrationConfig'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/approval-requests/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/approval-requests/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/approval-requests-GET': {
        'parameters': [
            {
                'name': 'filter'
            },
            {
                'name': 'expand'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}/reviews-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'id'
            },
            {
                'name': 'kind'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/approval-requests/{id}/reviews-POST': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'kind'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/auditlog/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/auditlog-GET': {
        'parameters': [
            {
                'name': 'before'
            },
            {
                'name': 'after'
            },
            {
                'name': 'q'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'spec'
            },
        ]
    },
    '/api/v2/code-refs/repositories/{repo}/branch-delete-tasks-POST': {
        'parameters': [
            {
                'name': 'repo'
            },
        ]
    },
    '/api/v2/code-refs/repositories/{repo}/branches/{branch}/extinction-events-POST': {
        'parameters': [
            {
                'name': 'repo'
            },
            {
                'name': 'branch'
            },
        ]
    },
    '/api/v2/code-refs/repositories-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'sourceLink'
            },
            {
                'name': 'commitUrlTemplate'
            },
            {
                'name': 'hunkUrlTemplate'
            },
            {
                'name': 'type'
            },
            {
                'name': 'defaultBranch'
            },
        ]
    },
    '/api/v2/code-refs/repositories/{repo}-DELETE': {
        'parameters': [
            {
                'name': 'repo'
            },
        ]
    },
    '/api/v2/code-refs/repositories/{repo}/branches/{branch}-GET': {
        'parameters': [
            {
                'name': 'repo'
            },
            {
                'name': 'branch'
            },
            {
                'name': 'projKey'
            },
            {
                'name': 'flagKey'
            },
        ]
    },
    '/api/v2/code-refs/repositories/{repo}-GET': {
        'parameters': [
            {
                'name': 'repo'
            },
        ]
    },
    '/api/v2/code-refs/statistics-GET': {
        'parameters': [
        ]
    },
    '/api/v2/code-refs/statistics/{projectKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'flagKey'
            },
        ]
    },
    '/api/v2/code-refs/repositories/{repo}/branches-GET': {
        'parameters': [
            {
                'name': 'repo'
            },
        ]
    },
    '/api/v2/code-refs/extinctions-GET': {
        'parameters': [
            {
                'name': 'repoName'
            },
            {
                'name': 'branchName'
            },
            {
                'name': 'projKey'
            },
            {
                'name': 'flagKey'
            },
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
        ]
    },
    '/api/v2/code-refs/repositories-GET': {
        'parameters': [
            {
                'name': 'withBranches'
            },
            {
                'name': 'withReferencesForDefaultBranch'
            },
            {
                'name': 'projKey'
            },
            {
                'name': 'flagKey'
            },
        ]
    },
    '/api/v2/code-refs/repositories/{repo}-PATCH': {
        'parameters': [
            {
                'name': 'repo'
            },
        ]
    },
    '/api/v2/code-refs/repositories/{repo}/branches/{branch}-PUT': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'head'
            },
            {
                'name': 'syncTime'
            },
            {
                'name': 'repo'
            },
            {
                'name': 'branch'
            },
            {
                'name': 'updateSequenceId'
            },
            {
                'name': 'references'
            },
            {
                'name': 'commitTime'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/{contextKind}/{contextKey}/flags/{featureFlagKey}-PUT': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'contextKind'
            },
            {
                'name': 'contextKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'setting'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/context-kinds/{key}-PUT': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'key'
            },
            {
                'name': 'description'
            },
            {
                'name': 'version'
            },
            {
                'name': 'hideInTargeting'
            },
            {
                'name': 'archived'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/{id}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/flags/evaluate-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/context-attributes-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/{kind}/{key}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'kind'
            },
            {
                'name': 'key'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'continuationToken'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'includeTotalCount'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/context-attributes/{attributeName}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'attributeName'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/{id}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'id'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'continuationToken'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'includeTotalCount'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/context-kinds-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/search-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'continuationToken'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'continuationToken'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'includeTotalCount'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/search-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'continuationToken'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'continuationToken'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'includeTotalCount'
            },
        ]
    },
    '/api/v2/roles-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'key'
            },
            {
                'name': 'policy'
            },
            {
                'name': 'description'
            },
            {
                'name': 'basePermissions'
            },
        ]
    },
    '/api/v2/roles/{customRoleKey}-DELETE': {
        'parameters': [
            {
                'name': 'customRoleKey'
            },
        ]
    },
    '/api/v2/roles/{customRoleKey}-GET': {
        'parameters': [
            {
                'name': 'customRoleKey'
            },
        ]
    },
    '/api/v2/roles-GET': {
        'parameters': [
        ]
    },
    '/api/v2/roles/{customRoleKey}-PATCH': {
        'parameters': [
            {
                'name': 'patch'
            },
            {
                'name': 'customRoleKey'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/destinations/{projectKey}/{environmentKey}-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'name'
            },
            {
                'name': 'kind'
            },
            {
                'name': 'config'
            },
            {
                'name': 'true'
            },
        ]
    },
    '/api/v2/destinations/{projectKey}/{environmentKey}/{id}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/destinations-GET': {
        'parameters': [
        ]
    },
    '/api/v2/destinations/{projectKey}/{environmentKey}/{id}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/destinations/{projectKey}/{environmentKey}/{id}-PATCH': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'key'
            },
            {
                'name': 'color'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'defaultTtl'
            },
            {
                'name': 'secureMode'
            },
            {
                'name': 'defaultTrackEvents'
            },
            {
                'name': 'confirmChanges'
            },
            {
                'name': 'requireComments'
            },
            {
                'name': 'source'
            },
            {
                'name': 'critical'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'sort'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/mobileKey-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/apiKey-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'expiry'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}-PATCH': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}/iterations-POST': {
        'parameters': [
            {
                'name': 'hypothesis'
            },
            {
                'name': 'metrics'
            },
            {
                'name': 'treatments'
            },
            {
                'name': 'flags'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'experimentKey'
            },
            {
                'name': 'canReshuffleTraffic'
            },
            {
                'name': 'primarySingleMetricKey'
            },
            {
                'name': 'primaryFunnelKey'
            },
            {
                'name': 'randomizationUnit'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/experiments-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'key'
            },
            {
                'name': 'iteration'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'description'
            },
            {
                'name': 'maintainerId'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'experimentKey'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}/metrics/{metricKey}/results-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'experimentKey'
            },
            {
                'name': 'metricKey'
            },
            {
                'name': 'iterationId'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/experimentation-settings-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}/experiments/{environmentKey}/{metricKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'metricKey'
            },
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}/metric-groups/{metricGroupKey}/results-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'experimentKey'
            },
            {
                'name': 'metricGroupKey'
            },
            {
                'name': 'iterationId'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/experiments-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'expand'
            },
            {
                'name': 'lifecycleState'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/experimentation-settings-PUT': {
        'parameters': [
            {
                'name': 'randomizationUnits'
            },
            {
                'name': 'projectKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}-PATCH': {
        'parameters': [
            {
                'name': 'instructions'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'experimentKey'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/flag-status/{projectKey}/{featureFlagKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'env'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}/copy-POST': {
        'parameters': [
            {
                'name': 'source'
            },
            {
                'name': 'target'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'comment'
            },
            {
                'name': 'includedActions'
            },
            {
                'name': 'excludedActions'
            },
        ]
    },
    '/api/v2/flags/{projectKey}-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'key'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'description'
            },
            {
                'name': 'includeInSnippet'
            },
            {
                'name': 'clientSideAvailability'
            },
            {
                'name': 'variations'
            },
            {
                'name': 'temporary'
            },
            {
                'name': 'customProperties'
            },
            {
                'name': 'defaults'
            },
            {
                'name': 'purpose'
            },
            {
                'name': 'migrationSettings'
            },
            {
                'name': 'clone'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}/expiring-targets/{environmentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'featureFlagKey'
            },
        ]
    },
    '/api/v2/flag-statuses/{projectKey}/{environmentKey}/{featureFlagKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'featureFlagKey'
            },
        ]
    },
    '/api/v2/flags/{projectKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'env'
            },
            {
                'name': 'tag'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
            {
                'name': 'archived'
            },
            {
                'name': 'summary'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'compare'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}/expiring-user-targets/{environmentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'featureFlagKey'
            },
        ]
    },
    '/api/v2/flag-statuses/{projectKey}/{environmentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'env'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}/expiring-targets/{environmentKey}-PATCH': {
        'parameters': [
            {
                'name': 'instructions'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}/expiring-user-targets/{environmentKey}-PATCH': {
        'parameters': [
            {
                'name': 'instructions'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}-PATCH': {
        'parameters': [
            {
                'name': 'patch'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{flagKey}/environments/{environmentKey}/migration-safety-issues-POST': {
        'parameters': [
            {
                'name': 'instructions'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'flagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}/dependent-flags-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{environmentKey}/{featureFlagKey}/dependent-flags-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'featureFlagKey'
            },
        ]
    },
    '/api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'title'
            },
            {
                'name': 'description'
            },
            {
                'name': 'key'
            },
            {
                'name': 'integrationKey'
            },
            {
                'name': 'timestamp'
            },
            {
                'name': 'deepLink'
            },
            {
                'name': 'metadata'
            },
        ]
    },
    '/api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}/{id}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
        ]
    },
    '/api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}/{id}-PATCH': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}-POST': {
        'parameters': [
            {
                'name': 'integrationKey'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'comment'
            },
            {
                'name': 'instructions'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'featureFlagKey'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id}-PATCH': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'id'
            },
            {
                'name': 'comment'
            },
            {
                'name': 'instructions'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/followers-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers/{memberId}-PUT': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'memberId'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers/{memberId}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'memberId'
            },
        ]
    },
    '/api/v2/engineering-insights/charts/deployments/frequency-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'applicationKey'
            },
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
            {
                'name': 'bucketType'
            },
            {
                'name': 'bucketMs'
            },
            {
                'name': 'groupBy'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/engineering-insights/charts/flags/status-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'applicationKey'
            },
        ]
    },
    '/api/v2/engineering-insights/charts/lead-time-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'applicationKey'
            },
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
            {
                'name': 'bucketType'
            },
            {
                'name': 'bucketMs'
            },
            {
                'name': 'groupBy'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/engineering-insights/charts/releases/frequency-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'applicationKey'
            },
            {
                'name': 'hasExperiments'
            },
            {
                'name': 'global'
            },
            {
                'name': 'groupBy'
            },
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
            {
                'name': 'bucketType'
            },
            {
                'name': 'bucketMs'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/engineering-insights/charts/flags/stale-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'applicationKey'
            },
            {
                'name': 'groupBy'
            },
            {
                'name': 'maintainerId'
            },
            {
                'name': 'maintainerTeamKey'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/engineering-insights/deployment-events-POST': {
        'parameters': [
            {
                'name': 'version'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'applicationKey'
            },
            {
                'name': 'eventType'
            },
            {
                'name': 'applicationName'
            },
            {
                'name': 'applicationKind'
            },
            {
                'name': 'versionName'
            },
            {
                'name': 'eventTime'
            },
            {
                'name': 'eventMetadata'
            },
            {
                'name': 'deploymentMetadata'
            },
        ]
    },
    '/api/v2/engineering-insights/deployments/{deploymentID}-GET': {
        'parameters': [
            {
                'name': 'deploymentID'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/engineering-insights/deployments-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'applicationKey'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'expand'
            },
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
            {
                'name': 'after'
            },
            {
                'name': 'before'
            },
            {
                'name': 'kind'
            },
            {
                'name': 'status'
            },
        ]
    },
    '/api/v2/engineering-insights/deployments/{deploymentID}-PATCH': {
        'parameters': [
            {
                'name': 'deploymentID'
            },
        ]
    },
    '/api/v2/engineering-insights/flag-events-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'applicationKey'
            },
            {
                'name': 'query'
            },
            {
                'name': 'impactSize'
            },
            {
                'name': 'hasExperiments'
            },
            {
                'name': 'global'
            },
            {
                'name': 'expand'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
            {
                'name': 'after'
            },
            {
                'name': 'before'
            },
        ]
    },
    '/api/v2/engineering-insights/pull-requests-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'applicationKey'
            },
            {
                'name': 'status'
            },
            {
                'name': 'query'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'expand'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'from'
            },
            {
                'name': 'to'
            },
            {
                'name': 'after'
            },
            {
                'name': 'before'
            },
        ]
    },
    '/api/v2/engineering-insights/repositories/projects-PUT': {
        'parameters': [
            {
                'name': 'mappings'
            },
        ]
    },
    '/api/v2/engineering-insights/repositories-GET': {
        'parameters': [
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/engineering-insights/repositories/{repositoryKey}/projects/{projectKey}-DELETE': {
        'parameters': [
            {
                'name': 'repositoryKey'
            },
            {
                'name': 'projectKey'
            },
        ]
    },
    '/api/v2/engineering-insights/insights/group-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'key'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'applicationKeys'
            },
        ]
    },
    '/api/v2/engineering-insights/insights/groups/{insightGroupKey}-DELETE': {
        'parameters': [
            {
                'name': 'insightGroupKey'
            },
        ]
    },
    '/api/v2/engineering-insights/insights/groups/{insightGroupKey}-GET': {
        'parameters': [
            {
                'name': 'insightGroupKey'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/engineering-insights/insights/scores-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'applicationKey'
            },
        ]
    },
    '/api/v2/engineering-insights/insights/groups-GET': {
        'parameters': [
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'query'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/engineering-insights/insights/groups/{insightGroupKey}-PATCH': {
        'parameters': [
            {
                'name': 'insightGroupKey'
            },
        ]
    },
    '/api/v2/integrations/{integrationKey}-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'config'
            },
            {
                'name': 'integrationKey'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'statements'
            },
            {
                'name': 'true'
            },
            {
                'name': 'url'
            },
            {
                'name': 'apiKey'
            },
        ]
    },
    '/api/v2/integrations/{integrationKey}/{id}-DELETE': {
        'parameters': [
            {
                'name': 'integrationKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/integrations/{integrationKey}/{id}-GET': {
        'parameters': [
            {
                'name': 'integrationKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/integrations/{integrationKey}-GET': {
        'parameters': [
            {
                'name': 'integrationKey'
            },
        ]
    },
    '/api/v2/integrations/{integrationKey}/{id}-PATCH': {
        'parameters': [
            {
                'name': 'integrationKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}-POST': {
        'parameters': [
            {
                'name': 'config'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'integrationKey'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'true'
            },
            {
                'name': 'name'
            },
        ]
    },
    '/api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'integrationKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'integrationKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
        ]
    },
    '/api/v2/integration-capabilities/featureStore-GET': {
        'parameters': [
        ]
    },
    '/api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}-PATCH': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'integrationKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}/validate-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'integrationKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}-POST': {
        'parameters': [
            {
                'name': 'config'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'integrationKey'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'true'
            },
            {
                'name': 'name'
            },
        ]
    },
    '/api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'integrationKey'
            },
            {
                'name': 'integrationId'
            },
        ]
    },
    '/api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'integrationKey'
            },
            {
                'name': 'integrationId'
            },
        ]
    },
    '/api/v2/integration-capabilities/big-segment-store-GET': {
        'parameters': [
        ]
    },
    '/api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId}-PATCH': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'integrationKey'
            },
            {
                'name': 'integrationId'
            },
        ]
    },
    '/api/v2/metrics/{projectKey}-POST': {
        'parameters': [
            {
                'name': 'key'
            },
            {
                'name': 'kind'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'description'
            },
            {
                'name': 'name'
            },
            {
                'name': 'selector'
            },
            {
                'name': 'urls'
            },
            {
                'name': 'isActive'
            },
            {
                'name': 'isNumeric'
            },
            {
                'name': 'unit'
            },
            {
                'name': 'eventKey'
            },
            {
                'name': 'successCriteria'
            },
            {
                'name': 'randomizationUnits'
            },
            {
                'name': 'unitAggregationType'
            },
        ]
    },
    '/api/v2/metrics/{projectKey}/{metricKey}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'metricKey'
            },
        ]
    },
    '/api/v2/metrics/{projectKey}/{metricKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'metricKey'
            },
            {
                'name': 'expand'
            },
            {
                'name': 'versionId'
            },
        ]
    },
    '/api/v2/metrics/{projectKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/metrics/{projectKey}/{metricKey}-PATCH': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'metricKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/metric-groups-POST': {
        'parameters': [
            {
                'name': 'tags'
            },
            {
                'name': 'key'
            },
            {
                'name': 'name'
            },
            {
                'name': 'kind'
            },
            {
                'name': 'maintainerId'
            },
            {
                'name': 'metrics'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'description'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/metric-groups/{metricGroupKey}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'metricGroupKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/metric-groups/{metricGroupKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'metricGroupKey'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/metric-groups-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/metric-groups/{metricGroupKey}-PATCH': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'metricGroupKey'
            },
        ]
    },
    '/api/v2/oauth/clients-POST': {
        'parameters': [
            {
                'name': 'description'
            },
            {
                'name': 'name'
            },
            {
                'name': 'redirectUri'
            },
        ]
    },
    '/api/v2/oauth/clients/{clientId}-DELETE': {
        'parameters': [
            {
                'name': 'clientId'
            },
        ]
    },
    '/api/v2/oauth/clients/{clientId}-GET': {
        'parameters': [
            {
                'name': 'clientId'
            },
        ]
    },
    '/api/v2/oauth/clients-GET': {
        'parameters': [
        ]
    },
    '/api/v2/oauth/clients/{clientId}-PATCH': {
        'parameters': [
            {
                'name': 'clientId'
            },
        ]
    },
    '/api/v2/public-ip-list-GET': {
        'parameters': [
        ]
    },
    '/api/v2/openapi.json-GET': {
        'parameters': [
        ]
    },
    '/api/v2-GET': {
        'parameters': [
        ]
    },
    '/api/v2/versions-GET': {
        'parameters': [
        ]
    },
    '/api/v2/projects-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'key'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'includeInSnippetByDefault'
            },
            {
                'name': 'defaultClientSideAvailability'
            },
            {
                'name': 'environments'
            },
        ]
    },
    '/api/v2/projects/{projectKey}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flag-defaults-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
        ]
    },
    '/api/v2/projects-GET': {
        'parameters': [
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/projects/{projectKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flag-defaults-PATCH': {
        'parameters': [
            {
                'name': 'projectKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flag-defaults-PUT': {
        'parameters': [
            {
                'name': 'tags'
            },
            {
                'name': 'temporary'
            },
            {
                'name': 'booleanDefaults'
            },
            {
                'name': 'defaultClientSideAvailability'
            },
            {
                'name': 'projectKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}-PATCH': {
        'parameters': [
            {
                'name': 'projectKey'
            },
        ]
    },
    '/api/v2/account/relay-auto-configs-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'policy'
            },
        ]
    },
    '/api/v2/account/relay-auto-configs/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/account/relay-auto-configs/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/account/relay-auto-configs-GET': {
        'parameters': [
        ]
    },
    '/api/v2/account/relay-auto-configs/{id}/reset-POST': {
        'parameters': [
            {
                'name': 'id'
            },
            {
                'name': 'expiry'
            },
        ]
    },
    '/api/v2/account/relay-auto-configs/{id}-PATCH': {
        'parameters': [
            {
                'name': 'patch'
            },
            {
                'name': 'id'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/release-pipelines-POST': {
        'parameters': [
            {
                'name': 'key'
            },
            {
                'name': 'name'
            },
            {
                'name': 'phases'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'description'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'pipelineKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/release-pipelines-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'pipelineKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}-PATCH': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'pipelineKey'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{flagKey}/release-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'flagKey'
            },
        ]
    },
    '/api/v2/flags/{projectKey}/{flagKey}/release-PATCH': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'flagKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes-POST': {
        'parameters': [
            {
                'name': 'executionDate'
            },
            {
                'name': 'instructions'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'comment'
            },
            {
                'name': 'ignoreConflicts'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id}-PATCH': {
        'parameters': [
            {
                'name': 'instructions'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'id'
            },
            {
                'name': 'comment'
            },
            {
                'name': 'ignoreConflicts'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{environmentKey}-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'key'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'description'
            },
            {
                'name': 'unbounded'
            },
            {
                'name': 'unboundedContextKind'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/environments/{environmentKey}/segments/evaluate-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/contexts/{contextKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
            {
                'name': 'contextKey'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{segmentKey}/expiring-targets/{environmentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{segmentKey}/expiring-user-targets/{environmentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{environmentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/users/{userKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
            {
                'name': 'userKey'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/contexts-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
            {
                'name': 'included'
            },
            {
                'name': 'excluded'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{segmentKey}/expiring-targets/{environmentKey}-PATCH': {
        'parameters': [
            {
                'name': 'instructions'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{segmentKey}/expiring-user-targets/{environmentKey}-PATCH': {
        'parameters': [
            {
                'name': 'instructions'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}-PATCH': {
        'parameters': [
            {
                'name': 'patch'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/users-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
            {
                'name': 'included'
            },
            {
                'name': 'excluded'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/exports/{exportID}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
            {
                'name': 'exportID'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/imports/{importID}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
            {
                'name': 'importID'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/exports-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
        ]
    },
    '/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/imports-POST': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'segmentKey'
            },
            {
                'name': 'file'
            },
            {
                'name': 'mode'
            },
        ]
    },
    '/api/v2/tags-GET': {
        'parameters': [
            {
                'name': 'kind'
            },
            {
                'name': 'pre'
            },
            {
                'name': 'archived'
            },
        ]
    },
    '/api/v2/teams/{teamKey}/members-POST': {
        'parameters': [
            {
                'name': 'teamKey'
            },
            {
                'name': 'file'
            },
        ]
    },
    '/api/v2/teams-POST': {
        'parameters': [
            {
                'name': 'key'
            },
            {
                'name': 'name'
            },
            {
                'name': 'description'
            },
            {
                'name': 'customRoleKeys'
            },
            {
                'name': 'memberIDs'
            },
            {
                'name': 'permissionGrants'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/teams/{teamKey}-GET': {
        'parameters': [
            {
                'name': 'teamKey'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/teams/{teamKey}/roles-GET': {
        'parameters': [
            {
                'name': 'teamKey'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
        ]
    },
    '/api/v2/teams/{teamKey}/maintainers-GET': {
        'parameters': [
            {
                'name': 'teamKey'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
        ]
    },
    '/api/v2/teams-GET': {
        'parameters': [
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
            {
                'name': 'filter'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/teams/{teamKey}-DELETE': {
        'parameters': [
            {
                'name': 'teamKey'
            },
        ]
    },
    '/api/v2/teams/{teamKey}-PATCH': {
        'parameters': [
            {
                'name': 'instructions'
            },
            {
                'name': 'teamKey'
            },
            {
                'name': 'comment'
            },
            {
                'name': 'expand'
            },
        ]
    },
    '/api/v2/teams-PATCH': {
        'parameters': [
            {
                'name': 'instructions'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/users/{projectKey}/{userKey}/expiring-user-targets/{environmentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'userKey'
            },
            {
                'name': 'environmentKey'
            },
        ]
    },
    '/api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'userKey'
            },
        ]
    },
    '/api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags/{featureFlagKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'userKey'
            },
            {
                'name': 'featureFlagKey'
            },
        ]
    },
    '/api/v2/users/{projectKey}/{userKey}/expiring-user-targets/{environmentKey}-PATCH': {
        'parameters': [
            {
                'name': 'instructions'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'userKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags/{featureFlagKey}-PUT': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'userKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'setting'
            },
            {
                'name': 'comment'
            },
        ]
    },
    '/api/v2/users/{projectKey}/{environmentKey}/{userKey}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'userKey'
            },
        ]
    },
    '/api/v2/users/{projectKey}/{environmentKey}/{userKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'userKey'
            },
        ]
    },
    '/api/v2/users/{projectKey}/{environmentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'searchAfter'
            },
        ]
    },
    '/api/v2/user-search/{projectKey}/{environmentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'q'
            },
            {
                'name': 'limit'
            },
            {
                'name': 'offset'
            },
            {
                'name': 'after'
            },
            {
                'name': 'sort'
            },
            {
                'name': 'searchAfter'
            },
            {
                'name': 'filter'
            },
        ]
    },
    '/api/v2/user-attributes/{projectKey}/{environmentKey}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
        ]
    },
    '/api/v2/webhooks-POST': {
        'parameters': [
            {
                'name': 'url'
            },
            {
                'name': 'sign'
            },
            {
                'name': 'tags'
            },
            {
                'name': 'name'
            },
            {
                'name': 'secret'
            },
            {
                'name': 'statements'
            },
            {
                'name': 'true'
            },
        ]
    },
    '/api/v2/webhooks/{id}-DELETE': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/webhooks/{id}-GET': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/webhooks-GET': {
        'parameters': [
        ]
    },
    '/api/v2/webhooks/{id}-PATCH': {
        'parameters': [
            {
                'name': 'id'
            },
        ]
    },
    '/api/v2/templates-POST': {
        'parameters': [
            {
                'name': 'key'
            },
            {
                'name': 'description'
            },
            {
                'name': 'name'
            },
            {
                'name': 'workflowId'
            },
            {
                'name': 'stages'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'flagKey'
            },
        ]
    },
    '/api/v2/templates/{templateKey}-DELETE': {
        'parameters': [
            {
                'name': 'templateKey'
            },
        ]
    },
    '/api/v2/templates-GET': {
        'parameters': [
            {
                'name': 'summary'
            },
            {
                'name': 'search'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows-POST': {
        'parameters': [
            {
                'name': 'name'
            },
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'description'
            },
            {
                'name': 'maintainerId'
            },
            {
                'name': 'stages'
            },
            {
                'name': 'templateKey'
            },
            {
                'name': 'templateKey'
            },
            {
                'name': 'dryRun'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows/{workflowId}-DELETE': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'workflowId'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows/{workflowId}-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'workflowId'
            },
        ]
    },
    '/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows-GET': {
        'parameters': [
            {
                'name': 'projectKey'
            },
            {
                'name': 'featureFlagKey'
            },
            {
                'name': 'environmentKey'
            },
            {
                'name': 'status'
            },
            {
                'name': 'sort'
            },
        ]
    },
};
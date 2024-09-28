    {{- define “chart.name.version” -}}
    {{- printf “%s-%s” .Chart.Name .Chart.Version | replace “+” “_” | trunc 63 | trimSuffix “-” -}}
    {{- end -}}

    {{- define “chart.chart” -}}
    {{- printf “%s-%s” .Chart.Name .Values.nameOverride | replace “+” “_” | trunc 63 | trimSuffix “-” -}}
    {{- end -}}

    {{- define “chart.name” -}}
    {{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix “-” -}}
    {{- end -}}

    {{- define “chart.labels” -}}
    labels:
    chart: {{ template “chart.chart” .}}
    app.kubernetes.io/name: {{ include “chart.name” . }}
    helm.sh/charts: {{ include “chart.name” . }}
    app.kubernetes.io/instance: {{ .Release.Name }}
    app.kubernetes.io/managed-by: {{ .Release.Service }}
    {{- end -}}

    {{- define “chart.annotations” -}}
    {{- if .Values.global.annotations -}}
    annotations:
    {{- toYaml .Values.global.annotations | nindent 2 }}
    {{- end -}}
    {{- end -}}

    {{- define “chart.image” -}}
    “{{ .Values.global.repository}}/{{ .Values.image.name }}:{{ .Values.image.tag }}”
    {{- end -}}

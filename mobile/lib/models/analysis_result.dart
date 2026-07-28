class AnalysisResultModel {
  AnalysisResultModel({
    required this.id,
    required this.riskScore,
    required this.riskLevel,
    required this.labels,
    required this.explanation,
    required this.tip,
    required this.engine,
    this.engineScores = const {},
    this.urlScores = const [],
  });

  final int id;
  final double riskScore;
  final String riskLevel;
  final List<String> labels;
  final String explanation;
  final String tip;
  final String engine;
  final Map<String, double> engineScores;
  final List<Map<String, dynamic>> urlScores;

  factory AnalysisResultModel.fromJson(Map<String, dynamic> json) {
    final scores = <String, double>{};
    final raw = json['engine_scores'];
    if (raw is Map) {
      raw.forEach((k, v) => scores['$k'] = (v as num).toDouble());
    }
    return AnalysisResultModel(
      id: json['id'] as int,
      riskScore: (json['risk_score'] as num).toDouble(),
      riskLevel: '${json['risk_level']}',
      labels: (json['labels'] as List<dynamic>? ?? []).map((e) => '$e').toList(),
      explanation: '${json['explanation']}',
      tip: '${json['tip']}',
      engine: '${json['engine']}',
      engineScores: scores,
      urlScores: (json['url_scores'] as List<dynamic>? ?? [])
          .map((e) => Map<String, dynamic>.from(e as Map))
          .toList(),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../l10n/app_strings.dart';
import '../services/session.dart';

class ResultScreen extends StatelessWidget {
  const ResultScreen({super.key, required this.result});
  final Map<String, dynamic> result;

  Color _color(String level) {
    switch (level) {
      case 'critical':
        return const Color(0xFF8B1E1E);
      case 'high':
        return const Color(0xFFB45309);
      case 'medium':
        return const Color(0xFFA16207);
      default:
        return const Color(0xFF0F5C4C);
    }
  }

  @override
  Widget build(BuildContext context) {
    final t = AppStrings(context.watch<SessionState>().locale);
    final level = '${result['risk_level'] ?? 'low'}';
    final labels = (result['labels'] as List<dynamic>? ?? []).map((e) => '$e').toList();
    return Scaffold(
      appBar: AppBar(title: Text(t.risk)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: _color(level).withValues(alpha: 0.12),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '${t.risk}: ${level.toUpperCase()}',
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                        color: _color(level),
                        fontWeight: FontWeight.bold,
                      ),
                ),
                Text('Score: ${result['risk_score']} · ${result['engine']}'),
              ],
            ),
          ),
          const SizedBox(height: 16),
          Text(t.explanation, style: Theme.of(context).textTheme.titleMedium),
          Text('${result['explanation']}'),
          const SizedBox(height: 16),
          Text(t.tip, style: Theme.of(context).textTheme.titleMedium),
          Text('${result['tip']}'),
          const SizedBox(height: 16),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: labels
                .map((l) => Chip(label: Text(l)))
                .toList(),
          ),
        ],
      ),
    );
  }
}

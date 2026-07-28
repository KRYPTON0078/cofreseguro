import 'package:flutter/material.dart';

class EngineBreakdown extends StatelessWidget {
  const EngineBreakdown({super.key, required this.scores});
  final Map<String, double> scores;

  @override
  Widget build(BuildContext context) {
    if (scores.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: scores.entries
          .map((e) => ListTile(
                dense: true,
                title: Text(e.key),
                trailing: Text(e.value.toStringAsFixed(2)),
              ))
          .toList(),
    );
  }
}

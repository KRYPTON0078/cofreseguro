import 'package:flutter/material.dart';

class RiskChip extends StatelessWidget {
  const RiskChip({super.key, required this.level});
  final String level;

  Color get _color {
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
    return Chip(
      label: Text(level.toUpperCase()),
      backgroundColor: _color.withValues(alpha: 0.15),
      labelStyle: TextStyle(color: _color, fontWeight: FontWeight.bold),
    );
  }
}

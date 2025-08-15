import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/session.dart';

class TipsScreen extends StatelessWidget {
  const TipsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final locale = context.watch<SessionState>().locale;
    final tips = locale == 'pt'
        ? ['Nunca partilhe PIN ou OTP.', 'Abra a app oficial em vez de clicar em links.']
        : ['Never share your PIN or OTP.', 'Open the official app instead of tapping links.'];
    return ListView(children: [for (final t in tips) ListTile(leading: const Icon(Icons.lightbulb), title: Text(t))]);
  }
}

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../l10n/app_strings.dart';
import '../services/session.dart';

class TipsScreen extends StatelessWidget {
  const TipsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final pt = context.watch<SessionState>().isPt;
    final tips = pt
        ? const [
            'Nunca partilhe PIN ou OTP por SMS, WhatsApp ou chamada.',
            'Abra a app oficial em vez de clicar em links suspeitos.',
            'Prémios inesperados são quase sempre fraude.',
            'Confirme agentes apenas dentro da aplicação oficial.',
            'Em dúvida, pare e ligue para o apoio oficial.',
          ]
        : const [
            'Never share PIN or OTP by SMS, WhatsApp, or phone call.',
            'Open the official app instead of tapping unexpected links.',
            'Unexpected prizes are almost always scams.',
            'Confirm agents only inside the official app.',
            'When unsure, stop and call the official helpline.',
          ];
    final t = AppStrings(context.watch<SessionState>().locale);
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Text(t.tips, style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 12),
        ...tips.map(
          (tip) => Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(Icons.lightbulb_outline, color: Color(0xFF0F5C4C)),
                const SizedBox(width: 12),
                Expanded(child: Text(tip)),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

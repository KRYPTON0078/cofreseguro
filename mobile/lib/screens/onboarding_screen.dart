import 'package:flutter/material.dart';

class OnboardingScreen extends StatelessWidget {
  const OnboardingScreen({super.key, required this.onDone});
  final VoidCallback onDone;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: 48),
            Text('CofreSeguro', style: Theme.of(context).textTheme.headlineLarge),
            const SizedBox(height: 12),
            const Text('Paste suspicious mobile-money SMS, get a risk score, labels, and a safety tip — in English or Portuguese.'),
            const Spacer(),
            FilledButton(onPressed: onDone, child: const Text('Continue')),
          ],
        ),
      ),
    );
  }
}

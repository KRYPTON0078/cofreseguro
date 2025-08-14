import 'package:flutter/material.dart';

class ResultScreen extends StatelessWidget {
  const ResultScreen({super.key, required this.result});
  final Map<String, dynamic> result;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Risk result')),
      body: ListView(padding: const EdgeInsets.all(16), children: [
        Text('${result['risk_level']}'.toUpperCase(), style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
        Text('Score: ${result['risk_score']}'),
        Text('Engine: ${result['engine']}'),
        const SizedBox(height: 12),
        Text('${result['explanation']}'),
        const SizedBox(height: 12),
        Text('Tip: ${result['tip']}'),
      ]),
    );
  }
}

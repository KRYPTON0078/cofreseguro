import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_client.dart';
import '../services/session.dart';
import 'result_screen.dart';

class AnalyzeScreen extends StatefulWidget {
  const AnalyzeScreen({super.key});
  @override
  State<AnalyzeScreen> createState() => _AnalyzeScreenState();
}

class _AnalyzeScreenState extends State<AnalyzeScreen> {
  final controller = TextEditingController();
  bool loading = false;

  Future<void> _run() async {
    setState(() => loading = true);
    try {
      final session = context.read<SessionState>();
      final result = await context.read<ApiClient>().analyze(session.token!, controller.text, session.locale);
      if (!mounted) return;
      Navigator.of(context).push(MaterialPageRoute(builder: (_) => ResultScreen(result: result)));
    } finally {
      setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        const Text('Paste an SMS or message'),
        Expanded(child: TextField(controller: controller, maxLines: null, expands: true)),
        FilledButton(onPressed: loading ? null : _run, child: Text(loading ? 'Analyzing...' : 'Analyze')),
      ]),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import '../l10n/app_strings.dart';
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
  String? error;

  Future<void> _analyzeText() async {
    final session = context.read<SessionState>();
    final token = session.token;
    if (token == null || controller.text.trim().isEmpty) return;
    setState(() {
      loading = true;
      error = null;
    });
    try {
      final result = await context.read<ApiClient>().analyze(
            session.apiBase,
            token,
            controller.text.trim(),
            session.locale,
          );
      if (!mounted) return;
      await Navigator.of(context).push(
        MaterialPageRoute(builder: (_) => ResultScreen(result: result)),
      );
    } catch (e) {
      setState(() => error = e.toString());
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  Future<void> _analyzeImage() async {
    final session = context.read<SessionState>();
    final token = session.token;
    if (token == null) return;
    final picker = ImagePicker();
    final file = await picker.pickImage(source: ImageSource.gallery);
    if (file == null) return;
    setState(() {
      loading = true;
      error = null;
    });
    final api = context.read<ApiClient>();
    try {
      final bytes = await file.readAsBytes();
      final result = await api.analyzeImage(
            session.apiBase,
            token,
            bytes,
            file.name,
            session.locale,
          );
      if (!mounted) return;
      await Navigator.of(context).push(
        MaterialPageRoute(builder: (_) => ResultScreen(result: result)),
      );
    } catch (e) {
      setState(() => error = e.toString());
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final session = context.watch<SessionState>();
    final t = AppStrings(session.locale);
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(t.pasteSms, style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          Expanded(
            child: TextField(
              controller: controller,
              maxLines: null,
              expands: true,
              textAlignVertical: TextAlignVertical.top,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                alignLabelWithHint: true,
              ),
            ),
          ),
          if (error != null)
            Padding(
              padding: const EdgeInsets.only(top: 8),
              child: Text(error!, style: const TextStyle(color: Colors.red)),
            ),
          const SizedBox(height: 12),
          FilledButton(
            onPressed: loading ? null : _analyzeText,
            child: Text(loading ? '...' : t.checkRisk),
          ),
          const SizedBox(height: 8),
          OutlinedButton.icon(
            onPressed: loading ? null : _analyzeImage,
            icon: const Icon(Icons.image_outlined),
            label: Text(t.pickImage),
          ),
        ],
      ),
    );
  }
}

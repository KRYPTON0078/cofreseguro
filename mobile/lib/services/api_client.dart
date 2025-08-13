import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiClient {
  ApiClient({required this.baseUrl});
  final String baseUrl;

  Future<String> login(String email, String password) async {
    final resp = await http.post(
      Uri.parse('$baseUrl/v1/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );
    if (resp.statusCode != 200) throw Exception('login failed');
    return jsonDecode(resp.body)['access_token'] as String;
  }

  Future<Map<String, dynamic>> analyze(String token, String text, String locale) async {
    final resp = await http.post(
      Uri.parse('$baseUrl/v1/analyze'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({'text': text, 'locale': locale}),
    );
    if (resp.statusCode != 200) throw Exception('analyze failed');
    return jsonDecode(resp.body) as Map<String, dynamic>;
  }

  Future<List<dynamic>> history(String token) async {
    final resp = await http.get(
      Uri.parse('$baseUrl/v1/history'),
      headers: {'Authorization': 'Bearer $token'},
    );
    if (resp.statusCode != 200) throw Exception('history failed');
    return jsonDecode(resp.body) as List<dynamic>;
  }
}

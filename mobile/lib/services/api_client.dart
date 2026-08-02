import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:http/http.dart' show MultipartFile, MultipartRequest;

class ApiClient {
  ApiClient();

  Future<String> login(String baseUrl, String email, String password) async {
    final resp = await http.post(
      Uri.parse('$baseUrl/v1/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );
    if (resp.statusCode != 200) {
      throw Exception('login failed (${resp.statusCode})');
    }
    return jsonDecode(resp.body)['access_token'] as String;
  }

  Future<Map<String, dynamic>> analyze(
    String baseUrl,
    String token,
    String text,
    String locale,
  ) async {
    final resp = await http.post(
      Uri.parse('$baseUrl/v1/analyze'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({'text': text, 'locale': locale}),
    );
    if (resp.statusCode != 200) {
      throw Exception('analyze failed (${resp.statusCode})');
    }
    return jsonDecode(resp.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> analyzeImage(
    String baseUrl,
    String token,
    List<int> bytes,
    String filename,
    String locale,
  ) async {
    final req = MultipartRequest('POST', Uri.parse('$baseUrl/v1/analyze/image?locale=$locale'));
    req.headers['Authorization'] = 'Bearer $token';
    req.files.add(MultipartFile.fromBytes('file', bytes, filename: filename));
    final streamed = await req.send();
    final body = await streamed.stream.bytesToString();
    if (streamed.statusCode != 200) {
      throw Exception('image analyze failed (${streamed.statusCode})');
    }
    return jsonDecode(body) as Map<String, dynamic>;
  }

  Future<List<dynamic>> history(String baseUrl, String token) async {
    final resp = await http.get(
      Uri.parse('$baseUrl/v1/history'),
      headers: {'Authorization': 'Bearer $token'},
    );
    if (resp.statusCode != 200) {
      throw Exception('history failed (${resp.statusCode})');
    }
    return jsonDecode(resp.body) as List<dynamic>;
  }

  Future<Map<String, dynamic>> behaviour(String baseUrl, String token) async {
    final resp = await http.get(
      Uri.parse('$baseUrl/v1/behaviour/me'),
      headers: {'Authorization': 'Bearer $token'},
    );
    if (resp.statusCode != 200) {
      throw Exception('behaviour failed (${resp.statusCode})');
    }
    return jsonDecode(resp.body) as Map<String, dynamic>;
  }
}

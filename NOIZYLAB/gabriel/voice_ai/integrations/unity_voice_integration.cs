/*
 * 🎮 UNITY VOICE AI INTEGRATION
 * C# Script for Unity
 * GORUNFREE Protocol
 */

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.Text;
using Newtonsoft.Json;

public class VoiceAIIntegration : MonoBehaviour
{
    [Header("API Configuration")]
    public string apiKey = ""; // Set in Inspector
    public string serviceURL = "http://localhost:5000/api/generate";
    
    [Header("Voice Settings")]
    public string service = "gtts"; // gtts, edge, azure, elevenlabs
    public string language = "en";
    public AudioSource audioSource;
    
    [Header("Testing")]
    public string testText = "Hello from Unity!";
    
    // Generate voice from text
    public void GenerateVoice(string text)
    {
        StartCoroutine(GenerateVoiceCoroutine(text));
    }
    
    IEnumerator GenerateVoiceCoroutine(string text)
    {
        // Create request
        var request = new UnityWebRequest(serviceURL, "POST");
        byte[] bodyRaw = Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(new
        {
            text = text,
            service = service,
            language = language
        }));
        
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerAudioClip(serviceURL, AudioType.MPEG);
        request.SetRequestHeader("Content-Type", "application/json");
        
        yield return request.SendWebRequest();
        
        if (request.result == UnityWebRequest.Result.Success)
        {
            AudioClip clip = DownloadHandlerAudioClip.GetContent(request);
            audioSource.clip = clip;
            audioSource.Play();
            Debug.Log("✅ Voice generated and playing!");
        }
        else
        {
            Debug.LogError($"❌ Error: {request.error}");
        }
    }
    
    // Test button
    [ContextMenu("Test Voice Generation")]
    public void TestVoice()
    {
        GenerateVoice(testText);
    }
    
    // Batch generate
    public void BatchGenerate(string[] texts)
    {
        StartCoroutine(BatchGenerateCoroutine(texts));
    }
    
    IEnumerator BatchGenerateCoroutine(string[] texts)
    {
        foreach (string text in texts)
        {
            GenerateVoice(text);
            yield return new WaitForSeconds(2f); // Wait between generations
        }
    }
}


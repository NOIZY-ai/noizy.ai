/*
 * 🎮 UNREAL ENGINE VOICE AI INTEGRATION
 * C++ Header for Unreal Engine
 * GORUNFREE Protocol
 */

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Http.h"
#include "Sound/SoundWave.h"
#include "Components/AudioComponent.h"
#include "VoiceAIIntegration.generated.h"

UCLASS()
class YOURGAME_API AVoiceAIIntegration : public AActor
{
    GENERATED_BODY()
    
public:
    AVoiceAIIntegration();
    
    // API Configuration
    UPROPERTY(EditAnywhere, Category = "Voice AI")
    FString APIKey;
    
    UPROPERTY(EditAnywhere, Category = "Voice AI")
    FString ServiceURL = TEXT("http://localhost:5000/api/generate");
    
    // Voice Settings
    UPROPERTY(EditAnywhere, Category = "Voice AI")
    FString Service = TEXT("gtts");
    
    UPROPERTY(EditAnywhere, Category = "Voice AI")
    FString Language = TEXT("en");
    
    // Audio Component
    UPROPERTY(VisibleAnywhere, Category = "Voice AI")
    UAudioComponent* AudioComponent;
    
    // Generate voice from text
    UFUNCTION(BlueprintCallable, Category = "Voice AI")
    void GenerateVoice(const FString& Text);
    
    // Batch generate
    UFUNCTION(BlueprintCallable, Category = "Voice AI")
    void BatchGenerate(const TArray<FString>& Texts);
    
protected:
    virtual void BeginPlay() override;
    
private:
    void OnResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful);
    
    FHttpModule* HttpModule;
};

// Implementation
AVoiceAIIntegration::AVoiceAIIntegration()
{
    PrimaryActorTick.bCanEverTick = false;
    
    AudioComponent = CreateDefaultSubobject<UAudioComponent>(TEXT("AudioComponent"));
    HttpModule = &FHttpModule::Get();
}

void AVoiceAIIntegration::BeginPlay()
{
    Super::BeginPlay();
}

void AVoiceAIIntegration::GenerateVoice(const FString& Text)
{
    TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = HttpModule->CreateRequest();
    Request->OnProcessRequestComplete().BindUObject(this, &AVoiceAIIntegration::OnResponseReceived);
    
    Request->SetURL(ServiceURL);
    Request->SetVerb(TEXT("POST"));
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
    
    // Create JSON payload
    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
    JsonObject->SetStringField(TEXT("text"), Text);
    JsonObject->SetStringField(TEXT("service"), Service);
    JsonObject->SetStringField(TEXT("language"), Language);
    
    FString OutputString;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&OutputString);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);
    
    Request->SetContentAsString(OutputString);
    Request->ProcessRequest();
}

void AVoiceAIIntegration::OnResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
{
    if (bWasSuccessful && Response.IsValid())
    {
        // Process audio response
        TArray<uint8> AudioData = Response->GetContent();
        
        // Create sound wave from audio data
        USoundWave* SoundWave = NewObject<USoundWave>(this);
        // ... audio processing code ...
        
        if (AudioComponent)
        {
            AudioComponent->SetSound(SoundWave);
            AudioComponent->Play();
        }
        
        UE_LOG(LogTemp, Warning, TEXT("✅ Voice generated and playing!"));
    }
    else
    {
        UE_LOG(LogTemp, Error, TEXT("❌ Voice generation failed!"));
    }
}

void AVoiceAIIntegration::BatchGenerate(const TArray<FString>& Texts)
{
    for (const FString& Text : Texts)
    {
        GenerateVoice(Text);
        // Add delay between generations
    }
}


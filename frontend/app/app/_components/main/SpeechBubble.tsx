export interface SpeechBubbleProps {
    message: string | null | undefined;
}

export default function SpeechBubble({ message }: SpeechBubbleProps) {
    if (!message) {
        return null;
    }

    return (
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 p-4 bg-white opacity-90 text-gray-950 rounded-lg border-2 border-gray-800 border-solid w-1/2 text-center">
            {message}
        </div>
    );
}

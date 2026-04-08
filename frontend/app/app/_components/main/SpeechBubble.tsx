export interface SpeechBubbleProps {
    message: string | null | undefined;
}

export default function SpeechBubble({ message }: SpeechBubbleProps) {
    if (!message) {
        return null;
    }

    return (
        <div className="absolute top-1/32 left-1/2 -translate-x-1/2 p-4 bg-white opacity-90 text-gray-950 rounded-lg border-2 border-gray-800 border-solid w-1/2 text-center">
            {message}
            <div className="absolute left-1/2 -translate-x-1/2 bottom-[-1px] translate-y-full w-0 h-0 border-l-[20px] border-r-[20px] border-t-[26px] border-l-transparent border-r-transparent border-t-gray-800" />
            <div className="absolute left-1/2 -translate-x-1/2 bottom-0 translate-y-full w-0 h-0 border-l-[18px] border-r-[18px] border-t-[24px] border-l-transparent border-r-transparent border-t-white" />
        </div>
    );
}

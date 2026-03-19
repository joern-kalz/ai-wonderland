import { useState } from "react";
import NpcImage from "./NpcImage";
import ActionBar from "./ActionBar";
import SpeechBubble from "./SpeechBubble";
import TravelError from "./TravelError";
import { sendTalk } from "@/libs/sendTalk";
import { sendTravel } from "@/libs/sendTravel";
import LoadingSpinner from "./LoadingSpinner";

export interface MainProps {
    sessionToken: string;
}

export default function Main({ sessionToken }: MainProps) {
    const [npcMessage, setNpcMessage] = useState<string | null>(null);
    const [travelError, setTravelError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [travelId, setTravelId] = useState(0);

    const onAction = async (mode: 'talk' | 'travel', inputValue: string) => {
        setNpcMessage(null);
        setTravelError(null);
        setLoading(true);
        if (mode === 'talk') {
            const { message } = await sendTalk({ sessionToken, message: inputValue });
            setNpcMessage(message);
        } else {
            const response = await sendTravel({ sessionToken, destination: inputValue });
            if (response.type === 'not_a_character_error') {
                setTravelError(`"${inputValue}" is not the name of a character. Please enter a character name`);
            }
            setTravelId(travelId + 1);
        }
        setLoading(false);
    }

    return (
        <div className="relative aspect-square max-h-full max-w-full">
            <NpcImage sessionToken={sessionToken} travelId={travelId} />
            <TravelError message={travelError} />
            <SpeechBubble message={npcMessage} />
            <ActionBar onAction={onAction} loading={loading} />
            {loading && <LoadingSpinner />}
        </div>
    )
}
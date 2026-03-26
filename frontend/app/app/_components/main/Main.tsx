import { useState } from "react";
import NpcImage from "./NpcImage";
import ActionBar from "./ActionBar";
import SpeechBubble from "./SpeechBubble";
import TravelError from "./TravelError";
import EndOverlay from "./EndOverlay";
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
    const [mode, setMode] = useState<'talk' | 'travel'>('talk');
    const [gameEnd, setGameEnd] = useState(false);

    const onAction = async (actionMode: 'talk' | 'travel', inputValue: string) => {
        setNpcMessage(null);
        setTravelError(null);
        setLoading(true);
        if (actionMode === 'talk') {
            const { message, game_end } = await sendTalk({ sessionToken, message: inputValue });
            setNpcMessage(message);
            if (game_end) {
                setGameEnd(true);
            }
        } else {
            const response = await sendTravel({ sessionToken, destination: inputValue });
            if (response.type === 'not_a_character_error') {
                setTravelError(`"${inputValue}" is not the name of a character. Please enter a character name`);
            } else {
                setMode('talk');
            }
            setTravelId((prev) => prev + 1);
        }
        setLoading(false);
    }

    return (
        <div className="relative aspect-square max-h-full max-w-full">
            <NpcImage sessionToken={sessionToken} travelId={travelId} />
            <TravelError message={travelError} />
            <SpeechBubble message={npcMessage} />
            <ActionBar mode={mode} setMode={setMode} onAction={onAction} loading={loading} />
            {loading && <LoadingSpinner />}
            {gameEnd && <EndOverlay />}
        </div>
    )
}
import { useState } from "react";
import NpcImage from "./NpcImage";
import ActionBar from "./ActionBar";
import SpeechBubble from "./SpeechBubble";
import TravelError from "./TravelError";

export interface MainProps {
    sessionToken: string;
}

export default function Main({ sessionToken }: MainProps) {
    const [npcMessage, setNpcMessage] = useState<string | null>(null);
    const [travelError, setTravelError] = useState<string | null>(null);

    return (
        <div className="relative aspect-square max-h-full max-w-full">
            <NpcImage sessionToken={sessionToken} />
            <TravelError message={travelError} />
            <SpeechBubble message={npcMessage} />
            <ActionBar sessionToken={sessionToken} setNpcMessage={setNpcMessage} setTravelError={setTravelError} />
        </div>
    )
}
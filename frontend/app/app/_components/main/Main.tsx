import NpcImage from "./NpcImage";
import ActionBar from "./ActionBar";

export interface MainProps {
    sessionToken: string;
}

export default function Main({ sessionToken }: MainProps) {
    return (
        <div className="relative aspect-square max-h-full max-w-full">
            <NpcImage sessionToken={sessionToken} />
            <ActionBar sessionToken={sessionToken} />
        </div>
    )
}